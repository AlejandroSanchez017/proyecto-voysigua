from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import text
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException
from app.schemas.Seguridad.usuarios import UsuarioCreate, UsuarioUpdate, UsuarioResponse
from passlib.context import CryptContext
from ...utils.security import create_access_token, hash_password
from ...utils.email_utils import enviar_email
import bcrypt
import pyotp
import re

# Crear un objeto para el hashing de contraseñas
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# **Crear usuario usando procedimiento almacenado**
async def create_user(db: AsyncSession, user_data: UsuarioCreate):
    existing_user = await db.execute(text("SELECT 1 FROM usuarios WHERE username=:username"), {"username": user_data.username})
    if existing_user.scalars().first():
        raise HTTPException(status_code=400, detail="El usuario ya existe")

    hashed_password = hash_password(user_data.password)
    otp_secret = pyotp.random_base32()

    query = text("""
        CALL insertar_usuario(:cod_persona, :nombre, :password, :remember_token, 
                              :username, :estado, :primera_vez, :fecha_vencimiento, :otp_secret)
    """)
    
    await db.execute(query, {
        "cod_persona": user_data.cod_persona,
        "nombre": user_data.nombre,
        "password": hashed_password,
        "remember_token": None,
        "username": user_data.username,
        "estado": user_data.estado,
        "primera_vez": user_data.primera_vez,
        "fecha_vencimiento": user_data.fecha_vencimiento,
        "otp_secret": otp_secret
    })
    
    await db.commit()
    return {"message": "Usuario creado correctamente"}

# **Actualizar usuario**
async def update_user(db: AsyncSession, id: int, user_data: UsuarioUpdate):
    new_token = None  
    if user_data.password:
        user_data.password = hash_password(user_data.password)
        new_token = create_access_token(data={"sub": user_data.username})

    query = text("""
        CALL actualizar_usuario(:id, :cod_persona, :nombre, :password, :remember_token, 
                               :username, :estado, :primera_vez, :fecha_vencimiento, :otp_secret)
    """)
    
    await db.execute(query, {
        "id": id,
        **user_data.dict(),
        "remember_token": new_token if new_token else user_data.remember_token
    })
    await db.commit()
    return {"message": "Usuario actualizado correctamente"}

# **Eliminar usuario**
async def eliminar_usuario(db: AsyncSession, id: int):
    try:
        await db.execute(text("CALL eliminar_usuario(:id)"), {"id": id})
        await db.commit()
        return {"message": "Usuario eliminado correctamente"}
    except SQLAlchemyError as e:
        await db.rollback()
        raise HTTPException(status_code=400, detail=f"Error al eliminar usuario: {str(e)}")

# **Autenticar usuario**
async def autenticar_usuario(db: AsyncSession, username: str, password: str):
    user = await db.execute(text("SELECT password FROM usuarios WHERE username=:username"), {"username": username})
    user = user.mappings().first()

    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    hashed_password = user["password"]
    
    if not bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8')):
        raise HTTPException(status_code=401, detail="Contraseña incorrecta")
    return user

# **Obtener usuario por ID**
async def obtener_usuario_por_id(db: AsyncSession, id: int):
    result = await db.execute(text("CALL obtener_usuario_por_id(:id)"), {"id": id})
    return result.mappings().first()

# **Obtener todos los usuarios**
async def obtener_todos_los_usuarios(db: AsyncSession, skip: int = 0, limit: int = 10):
    result = await db.execute(text("CALL obtener_todos_los_usuarios(:skip, :limit)"), {"skip": skip, "limit": limit})
    return result.mappings().all()

# **Generar OTP**
async def generar_otp(db: AsyncSession, username: str):
    user = await db.execute(text("SELECT otp_secret, cod_persona FROM usuarios WHERE username=:username"), {"username": username})
    user = user.mappings().first()
    
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    persona = await db.execute(text("SELECT correo FROM tbl_personas WHERE cod_persona=:cod_persona"), {"cod_persona": user['cod_persona']})
    persona = persona.mappings().first()
    
    if not persona or not persona['correo']:
        raise HTTPException(status_code=400, detail="No se encontró el correo electrónico del usuario")
    
    email = str(persona['correo']).strip().lower()
    
    email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not re.match(email_regex, email):
        raise HTTPException(status_code=400, detail=f"El email obtenido no es válido: {email}")
    
    if not user['otp_secret']:
        user['otp_secret'] = pyotp.random_base32()
        await db.execute(text("UPDATE usuarios SET otp_secret=:otp_secret WHERE username=:username"), {"otp_secret": user['otp_secret'], "username": username})
        await db.commit()
    
    totp = pyotp.TOTP(user['otp_secret'], interval=120)
    otp_code = totp.now()
    
    success = enviar_email(email, otp_code)
    
    if success:
        return {"message": "Código OTP enviado correctamente"}
    else:
        raise HTTPException(status_code=500, detail="Error al enviar el correo")
    
    
# **Obtener usuario por username**
async def obtener_email_por_usuario(db: AsyncSession, username: str):
    result = await db.execute(text("SELECT correo FROM usuarios WHERE username=:username"), {"username": username})
    return result.scalar()

# **Verificar OTP**
async def verificar_otp(db: AsyncSession, username: str, user_otp: str):
    user = await db.execute(text("SELECT otp_secret FROM usuarios WHERE username=:username"), {"username": username})
    user = user.mappings().first()
    
    if not user or not user['otp_secret']:
        raise HTTPException(status_code=404, detail="Usuario no tiene 2FA activado")
    
    totp = pyotp.TOTP(user['otp_secret'], interval=120)
    
    if not totp.verify(user_otp):
        raise HTTPException(status_code=401, detail="Código OTP inválido")
    
    return {"message": "OTP válido, autenticación completada"}

