from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from sqlalchemy.sql import select
from app.database import get_async_db, get_sync_db
from app.crud.Seguridad.Usuarios import (obtener_todos_los_usuarios, insertar_usuario, actualizar_usuario, eliminar_usuario,autenticar_usuario,generar_otp,verificar_otp,
    obtener_usuario_por_id, 
)
from app.schemas.Seguridad.Usuarios import UsuarioCreate, UsuarioUpdate, UsuarioResponse, LoginSchema, OTPVerifySchema, UsuarioAuthResponse
from app.models.Seguridad.Usuarios import Usuario
from app.utils.security import create_access_token
from app.utils.email_utils import enviar_email
from typing import List
import logging

# Configurar logging
logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)

router = APIRouter()

# ✅ Ruta para obtener todas las personas (SÍNCRONA)
@router.get("/usuarios/", response_model=List[UsuarioAuthResponse])
async def obtener_todos_los_usuarios(db: AsyncSession = Depends(get_async_db)):
    result = await db.execute(select(Usuario))  # ✅ Obtiene `remember_token`
    usuarios = result.scalars().all()

    return [UsuarioAuthResponse.model_validate(user.__dict__) for user in usuarios]


# ✅ Endpoint para insertar un nuevo usuario (ASÍNCRONO)
@router.post("/usuarios/", response_model=UsuarioResponse)
async def crear_usuario(usuario: UsuarioCreate, db: AsyncSession = Depends(get_async_db)):
    try:
        usuario_creado = await insertar_usuario(db, usuario)
        return usuario_creado  # ✅ Devuelve `UsuarioResponse`
    except Exception as e:
        error_message = str(e.orig) if hasattr(e, 'orig') else str(e)
        logger.error(f"Error al insertar usuario: {error_message}")
        raise HTTPException(status_code=400, detail=error_message)



# ✅ Endpoint para actualizar un usuario (ASÍNCRONO)
@router.put("/usuarios/{id}", response_model=dict)
async def modificar_usuario(id: int, usuario: UsuarioUpdate, db: AsyncSession = Depends(get_async_db)):
    try:
        response = await actualizar_usuario(db, id, usuario.dict(exclude_unset=True))  # Solo enviar valores proporcionados
        return response
    except Exception as e:
        logger.error(f"Error al actualizar usuario {id}: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))


# ✅ Endpoint para eliminar un usuario (ASÍNCRONO)
@router.delete("/usuarios/{id}", response_model=dict)
async def borrar_usuario(id: int, db: AsyncSession = Depends(get_async_db)):
    usuario_eliminado = await eliminar_usuario(db, id)
    if usuario_eliminado is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    return {"message": f"Usuario con ID {id} eliminado correctamente"}


# ✅ Endpoint para obtener un usuario por ID (ASÍNCRONO)
@router.get("/usuarios/{id}", response_model=UsuarioResponse)
async def obtener_usuario(id: int, db: AsyncSession = Depends(get_async_db)):
    usuario = await obtener_usuario_por_id(db, id)
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return UsuarioResponse.model_validate(usuario)

# ✅ Endpoint para iniciar sesión y obtener un token de acceso (ASÍNCRONO)
@router.post("/login")
async def login(login: LoginSchema, db: AsyncSession = Depends(get_async_db)):
    user = await autenticar_usuario(db, login.username, login.password)

    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Credenciales inválidas")

    # Generar código OTP y actualizar en la base de datos
    otp_response = await generar_otp(db, login.username)
    # Generar token JWT (si lo deseas)
    access_token = create_access_token({"sub": user.username})

    return {
        "message": "Se ha enviado un código OTP a tu correo electrónico. Ingrese el código para completar el login.",
        "otp_expires_in": 120  # Opcional: Indica el tiempo de validez del OTP
    }

# ✅ Endpoint para verificar OTP (ASÍNCRONO)
@router.post("/verify-otp")
async def verify_otp(data: OTPVerifySchema, db: AsyncSession = Depends(get_async_db)):
    otp_valid = await verificar_otp(db, data.username, data.otp_code)

    if not otp_valid:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Código OTP inválido o expirado")

    # Generar token JWT después de verificar el OTP
    access_token = create_access_token(data={"sub": data.username})

    return {
        "message": "✅ Autenticación exitosa",
        "access_token": access_token,
        "token_type": "bearer"
    }
