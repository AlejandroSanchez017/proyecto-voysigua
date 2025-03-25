from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import select, text
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException
from app.schemas.Seguridad.Usuarios import UsuarioCreate, UsuarioUpdate, UsuarioResponse
from app.models.Seguridad.Usuarios import Usuario
from app.models.Personas.personas import Persona
from app.utils.security import create_access_token, hash_password
from app.utils.email_utils import enviar_email
import pyotp
import secrets
import bcrypt


# Obtener todas los usuarios
async def obtener_todos_los_usuarios(db: AsyncSession, skip: int = 0, limit: int = 10):
    result = await db.execute(select(Usuario).offset(skip).limit(limit))
    return result.scalars().all()


async def insertar_usuario(db: AsyncSession, user_data: UsuarioCreate):
    # Verificar si el usuario ya existe
    result = await db.execute(select(Usuario).filter(Usuario.username == user_data.username))
    existing_user = result.scalars().first()

    # Generar el hash de la contraseña antes de asignarlo
    hashed_password = hash_password(user_data.password)  # ✅ Se asegura de que siempre tenga un valor

    user_data.password = hashed_password

    # Generar un secreto OTP para el usuario
    otp_secret = pyotp.random_base32()

    # Crear la instancia del usuario en la BD con el otp_secret
    new_user = Usuario(**user_data.dict(), otp_secret=otp_secret)

    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)  # Obtener los datos actualizados desde la BD

    # 🔹 Conversión explícita a UsuarioResponse antes de devolverlo
    return UsuarioResponse.model_validate(new_user._dict_)



# Obtener usuario por ID (asíncrono)
async def obtener_usuario_por_id(db: AsyncSession, id: int):
    usuario = await db.get(Usuario, id)
    return usuario if usuario else None


# ✅ Actualizar usuario (asíncrono) con procedimiento almacenado
async def actualizar_usuario(db: AsyncSession, id: int, user_data: dict):
    user = await db.get(Usuario, id)
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    new_token = None  # Variable para guardar el nuevo token si cambia password o username

    # 🔹 Si se proporciona una nueva contraseña, la encriptamos y generamos un nuevo token
    if "password" in user_data and user_data["password"]:
        user_data["password"] = hash_password(user_data["password"])
        new_token = create_access_token(data={"sub": user.username})  

    # 🔹 Si el username cambia, generamos un nuevo token
    if "username" in user_data and user.username != user_data["username"]:
        new_token = create_access_token(data={"sub": user_data["username"]})

    # 🔹 Si hay un nuevo token, lo guardamos en user_data para enviarlo a PostgreSQL
    if new_token:
        user_data["remember_token"] = new_token if isinstance(new_token, str) else new_token.get("access_token")

    # 🔹 Llamar al procedimiento almacenado en PostgreSQL
    stmt = text("""
        CALL actualizar_usuario(
            :id, :nombre, :password, :username, :estado, :remember_token
        )
    """)

    await db.execute(stmt, {
        "id": id,
        "nombre": user_data.get("nombre"),
        "password": user_data.get("password"),
        "username": user_data.get("username"),
        "estado": user_data.get("estado"),
        "remember_token": user_data.get("remember_token")  # Ahora lo enviamos al procedimiento
    })

    await db.commit()
    return {
        "message": "Usuario actualizado correctamente",
        "new_token": user_data.get("remember_token") if new_token else "No se generó un nuevo token"
    }


# Eliminar usuario (asíncrono)
async def eliminar_usuario(db: AsyncSession, id: int):
    async with db.begin():
        db_usuario = await db.get(Usuario, id)
        if not db_usuario:
            return None
        await db.delete(db_usuario)
        await db.commit()
        return db_usuario



#----------------------------------------------------------------------------------------------------------------

# Obtener usuario por username (asíncrono)
async def obtener_email_por_usuario(db: AsyncSession, username: str):
    result = await db.execute(select(Usuario).filter(Usuario.username == username))
    return result.scalars().first()

# Autenticar usuario (asíncrono)
async def autenticar_usuario(db: AsyncSession, username: str, password: str):
    user = await obtener_email_por_usuario(db, username)

    if not user or not user.password:
        return None

    if bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
        # Genera y guarda remember_token aquí mismo
        remember_token = secrets.token_hex(32)
        user.remember_token = remember_token

        db.add(user)
        await db.commit()
        await db.refresh(user)

        return user

    return None


# Generar OTP y enviarlo por email (asíncrono)
async def generar_otp(db: AsyncSession, username: str):
    user = await obtener_email_por_usuario(db, username)  # Cambio de función

    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    persona = await db.get(Persona, user.cod_persona)

    if not persona or not persona.correo:
        raise HTTPException(status_code=400, detail="No se encontró el correo electrónico del usuario")

    email = persona.correo

    # Si ya tiene un OTP secreto, reutilizarlo
    if not user.otp_secret:
        user.otp_secret = pyotp.random_base32()
        await db.commit()

    totp = pyotp.TOTP(user.otp_secret, interval=120)
    otp_code = totp.now()

    success = enviar_email(email, otp_code)
    
    if success:
        return {"message": "Código OTP enviado correctamente"}
    raise HTTPException(status_code=500, detail="Error al enviar el correo")


# Verificar OTP (asíncrono)
async def verificar_otp(db: AsyncSession, username: str, user_otp: str):
    user = await obtener_email_por_usuario(db, username)  # Cambio de función

    if not user or not user.otp_secret:
        raise HTTPException(status_code=404, detail="Usuario no tiene 2FA activado")

    totp = pyotp.TOTP(user.otp_secret, interval=120)

    if not totp.verify(user_otp):
        raise HTTPException(status_code=401, detail="Código OTP inválido")
    
    return {"message": "OTP válido, autenticación completada"}