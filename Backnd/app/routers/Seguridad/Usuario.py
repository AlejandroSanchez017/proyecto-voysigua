from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from ...crud.Seguridad.Usuarios import (
    obtener_email_por_usuario, verificar_otp, autenticar_usuario, generar_otp, 
    create_user, update_user, eliminar_usuario, obtener_usuario_por_id, 
    obtener_todos_los_usuarios as crud_obtener_todos_los_usuarios
)
from app.schemas.Seguridad.usuarios import UsuarioResponse, UsuarioCreate, UsuarioUpdate, LoginSchema, OTPVerifySchema
from app.utils.security import create_access_token, get_current_user
from app.utils.email_utils import enviar_email
from app.database import get_sync_db, get_async_db
from typing import List
from datetime import datetime

# Crear una instancia de CryptContext para manejar la encriptación de contraseñas
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

router = APIRouter()

#  Endpoint para actualizar un usuario existente
@router.put("/usuarios/{id}")
async def modificar_usuario(id: int, usuario: UsuarioUpdate, db: AsyncSession = Depends(get_async_db)):
    try:
        usuario_dict = usuario.dict(exclude_unset=True)
        response = await update_user(db, id, usuario_dict)
        return response
    except Exception as e:
        import traceback
        error_message = traceback.format_exc()
        raise HTTPException(status_code=400, detail=str(error_message))

#  Endpoint para eliminar un usuario
@router.delete("/usuarios/{id}")
async def borrar_usuario(id: int, db: AsyncSession = Depends(get_async_db)):
    try:
        usuario_eliminado = await eliminar_usuario(db, id)
        if usuario_eliminado is None:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")
        return {"message": "Usuario eliminado correctamente"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# Ruta para obtener un usuario por ID
@router.get("/usuarios/{id}", response_model=UsuarioResponse)
async def obtener_usuario(id: int, db: AsyncSession = Depends(get_sync_db)):
    usuario = await obtener_usuario_por_id(db, id)

    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    return usuario

#  Ruta para obtener todos los usuarios
@router.get("/usuarios", response_model=List[UsuarioResponse])  
async def obtener_todos_los_usuarios(skip: int = 0, limit: int = 10, db: AsyncSession = Depends(get_async_db)):
    usuarios = await crud_obtener_todos_los_usuarios(db, skip, limit)
    return usuarios

# Endpoint para iniciar sesión y obtener un token de acceso
@router.post("/login")
async def login(login: LoginSchema, db: AsyncSession = Depends(get_sync_db)):
    user = await autenticar_usuario(db, login.username, login.password)

    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Credenciales inválidas")

    # Obtener email del usuario
    email = await obtener_email_por_usuario(db, login.username)
    if not email:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No se encontró el correo del usuario")
    
    # Generar código OTP
    otp_code = await generar_otp(db, login.username)
    if not otp_code:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="No se pudo generar el código OTP")
    
    # Enviar código OTP por email
    await enviar_email(email, otp_code)
    
    return {"message": "Se ha enviado un código OTP a tu correo electrónico. Ingrese el código para completar el login."}

@router.post("/verify-otp")
async def verify_otp(data: OTPVerifySchema, db: AsyncSession = Depends(get_sync_db)):
    # Buscar el usuario en la base de datos
    result = await db.execute(select(Usuario).filter(Usuario.username == data.username))
    user = result.scalars().first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuario no encontrado")

    # Verificar si el OTP es correcto
    is_valid = await verificar_otp(db, data.username, data.otp_code)
    if not is_valid:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Código OTP inválido")

    # Generar el token JWT
    access_token = create_access_token(data={"sub": data.username})

    # ✅ Guarda solo el token como string
    user.remember_token = str(access_token)
    await db.commit()

    return {
        "message": "✅ Autenticación exitosa",
        "access_token": access_token,
        "token_type": "bearer"
    }

#  Ruta protegida (requiere autenticación)
@router.get("/usuarios/protected", response_model=UsuarioResponse)
async def protected_route(current_user: UsuarioResponse = Depends(get_current_user)):
    return current_user

# Crear un nuevo usuario con contraseña cifrada y token
@router.post("/usuarios/")
async def crear_usuario(usuario: UsuarioCreate, db: AsyncSession = Depends(get_async_db)):
    try:
        # Intenta crear el usuario directamente con SQLAlchemy
        new_user = await create_user(db, usuario)

        # Generar el token de acceso para el usuario recién creado
        access_token = create_access_token(data={"sub": new_user.username})

        return {"message": "Usuario insertado correctamente", "access_token": access_token}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
