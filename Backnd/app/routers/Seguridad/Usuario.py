from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ...models.Seguridad.Usuarios import Usuario
from ...crud.Seguridad.Usuarios import (
    obtener_email_por_usuario, verificar_otp, autenticar_usuario, generar_otp, create_user, update_user, eliminar_usuario, obtener_todos_los_usuarios_por_id, obtener_todos_los_usuarios as crud_obtener_todos_los_usuarios)
from ...schemas.Seguridad.Usuarios import UsuarioResponse, UsuarioCreate, UsuarioUpdate, LoginSchema, OTPVerifySchema
from ...utils.security import  create_access_token, get_current_user
from ...utils.email_utils import enviar_email
from ...database import get_db
from typing import List 

# Crear una instancia de CryptContext para manejar la encriptación de contraseñas
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

router = APIRouter()

#  Endpoint para actualizar un usuario existente
@router.put("/usuarios/{id}")
def modificar_usuario(id: int, usuario: UsuarioUpdate, db: Session = Depends(get_db)):
    try:
        usuario_dict = usuario.dict(exclude_unset=True)
        response = update_user(db, id, usuario_dict)
        return response
    except Exception as e:
        import traceback
        error_message = traceback.format_exc()  # 🔍 Captura el error completo
        raise HTTPException(status_code=400, detail=str(error_message))

#  Endpoint para eliminar un usuario
@router.delete("/usuarios/{id}")
def borrar_usuario(id: int, db: Session = Depends(get_db)):
    try:
        usuario_eliminado = eliminar_usuario(db, id)
        if usuario_eliminado is None:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")
        return {"message": "Usuario eliminado correctamente"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# Ruta para obtener un usuario por ID
@router.get("/usuarios/{id}", response_model=UsuarioResponse)
def obtener_usuario(id: int, db: Session = Depends(get_db)):
    usuario = obtener_todos_los_usuarios_por_id(db, id)
    
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

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



#  Ruta para obtener todos los usuarios
@router.get("/usuarios", response_model=List[UsuarioResponse])  
def obtener_todos_los_usuarios(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    usuarios = db.query(Usuario).offset(skip).limit(limit).all()
    return usuarios 

# Endpoint para iniciar sesión y obtener un token de acceso
@router.post("/login")
def login(login: LoginSchema, db: Session = Depends(get_db)):
    user = autenticar_usuario(db, login.username, login.password)
    
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Credenciales inválidas")

    # Obtener email del usuario
    email = obtener_email_por_usuario(db, login.username)
    if not email:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No se encontró el correo del usuario")
    
    # Generar código OTP
    otp_code = generar_otp(db, login.username)
    if not otp_code:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="No se pudo generar el código OTP")
    
    # Enviar código OTP por email
    enviar_email(email, otp_code)
    
    return {"message": "Se ha enviado un código OTP a tu correo electrónico. Ingrese el código para completar el login."}

@router.post("/verify-otp")
def verify_otp(data: OTPVerifySchema, db: Session = Depends(get_db)):
    # Buscar el usuario en la base de datos
    user = db.query(Usuario).filter(Usuario.username == data.username).first()
    
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuario no encontrado")

    # Verificar si el OTP es correcto
    if not verificar_otp(db, data.username, data.otp_code):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Código OTP inválido")

    # Generar el token JWT
    access_token = create_access_token(data={"sub": data.username})

    # ❌ ERROR: Estás guardando un diccionario en `remember_token`
    # user.remember_token = {"access_token": access_token, "token_type": "bearer", "expires_in": str(datetime.utcnow())}

    # ✅ SOLUCIÓN: Guarda solo el string del token
    user.remember_token = str(access_token)  # Guarda solo el token como un string
    db.commit()

    return {
        "message": "✅ Autenticación exitosa",
        "access_token": access_token,
        "token_type": "bearer"
    }



#  Ruta protegida (requiere autenticación)
@router.get("/usuarios/protected", response_model=UsuarioResponse)
def protected_route(current_user: UsuarioResponse = Depends(get_current_user)):
    return current_user

# Crear un nuevo usuario con contraseña cifrada y token
@router.post("/usuarios/")
def crear_usuario(usuario: UsuarioCreate, db: Session = Depends(get_db)):
    try:
        # Intenta crear el usuario directamente con SQLAlchemy
        new_user = create_user(db, usuario)

        # Generar el token de acceso para el usuario recién creado
        access_token = create_access_token(data={"sub": new_user.username})

        return {"message": "Usuario insertado correctamente", "access_token": access_token}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

