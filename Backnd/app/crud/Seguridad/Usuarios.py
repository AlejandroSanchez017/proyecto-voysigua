from sqlalchemy.orm import Session
from sqlalchemy.sql import text
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException
from ...schemas.Seguridad.Usuarios import UsuarioCreate, UsuarioUpdate, UsuarioResponse
from ...models.Seguridad.Usuarios import Usuario
from passlib.context import CryptContext
from ...utils.security import create_access_token,hash_password
from datetime import timedelta

# Crear un objeto para el hashing de contraseñas
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# **Actualizar usuario**
def update_user(db: Session, id: int, user_data: dict):
    user = db.query(Usuario).filter(Usuario.id == id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    # Variable para saber si se debe generar un nuevo token
    new_token = None  

    # 🔐 Encriptar la nueva contraseña solo si se proporciona
    if "password" in user_data and user_data["password"]:
        user_data["password"] = hash_password(user_data["password"])
        new_token = create_access_token(data={"sub": user.username})  # 🔄 Generar token si cambia la contraseña

    # 🔄 Generar un nuevo token si el username cambia
    if "username" in user_data and user.username != user_data["username"]:
        new_token = create_access_token(data={"sub": user_data["username"]})

    # ✅ Si se generó un nuevo token, actualizarlo en la base de datos
    if new_token:
        user_data["remember_token"] = new_token  # ⚠️ Aquí se debe extraer solo el `access_token`
        if isinstance(new_token, dict):  # Si `create_access_token` devuelve un diccionario
            user_data["remember_token"] = new_token.get("access_token")  # Extraer solo el token

    # 📝 Actualizar solo los campos enviados
    update_data = {k: v for k, v in user_data.items() if v is not None}
    db.query(Usuario).filter(Usuario.id == id).update(update_data)
    
    db.commit()
    db.refresh(user)  # ✅ Sincronizar con la BD

    return {"message": "Usuario actualizado correctamente", "new_token": user_data.get("remember_token")}



# **Eliminar usuario**
def eliminar_usuario(db: Session, id: int):
    try:
        db_usuario = db.query(Usuario).filter(Usuario.id == id).first()
        if db_usuario is None:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")

        db.delete(db_usuario)
        db.commit()
        return db_usuario
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"Error al eliminar usuario: {str(e)}")

# **Obtener usuario por ID**
def obtener_todos_los_usuarios_por_id(db: Session, id: int):
    usuario = db.query(Usuario).filter(Usuario.id == id).first()
    
    # 🔍 Agregar un print para ver si el usuario se encuentra
    print("Usuario encontrado en la base de datos:", usuario)

    if not usuario:
        return None  
    
    return UsuarioResponse( 
        id=usuario.id,
        cod_persona=usuario.cod_persona,
        nombre=usuario.nombre,
        remember_token=usuario.remember_token,
        username=usuario.username,
        preguntas_contestadas=usuario.preguntas_contestadas,
        estado=usuario.estado,
        primera_vez=usuario.primera_vez,
        fecha_vencimiento=usuario.fecha_vencimiento,
        intentos_preguntas=usuario.intentos_preguntas,
        preguntas_correctas=usuario.preguntas_correctas
    )


# **Obtener todos los usuarios**
def obtener_todos_los_usuarios(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Usuario).offset(skip).limit(limit).all()

# **Insertar un nuevo usuario (encriptando la contraseña)**
def create_user(db: Session, user_data: UsuarioCreate):
    # Verificar si el usuario ya existe
    existing_user = db.query(Usuario).filter(Usuario.username == user_data.username).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="El usuario ya existe")

    # Hashear la contraseña antes de guardarla
    hashed_password = hash_password(user_data.password)
    user_data.password = hashed_password

    # Crear la instancia del usuario en la BD
    new_user = Usuario(**user_data.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)  # Refrescar para obtener datos actualizados de la BD

    # Retornar el usuario sin exponer la contraseña
    return UsuarioResponse(
        id=new_user.id,
        cod_persona=new_user.cod_persona,
        nombre=new_user.nombre,
        remember_token=new_user.remember_token,
        username=new_user.username,
        preguntas_contestadas=new_user.preguntas_contestadas,
        estado=new_user.estado,
        primera_vez=new_user.primera_vez,
        fecha_vencimiento=new_user.fecha_vencimiento,
        intentos_preguntas=new_user.intentos_preguntas,
        preguntas_correctas=new_user.preguntas_correctas
    )


