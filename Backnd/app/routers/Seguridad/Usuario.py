from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from sqlalchemy.sql import select
from app.database import get_async_db, get_sync_db
from app.crud.Seguridad.Usuarios import (obtener_todos_los_usuarios, insertar_usuario, actualizar_usuario, eliminar_usuario,autenticar_usuario,generar_otp,verificar_otp,
    obtener_usuario_por_id, obtener_email_por_usuario, obtener_usuario_por_username
)
from app.crud.Seguridad.model_to_rol import (consultar_roles_por_modelo_crud)
from app.crud.Seguridad.model_to_permission import (consultar_permisos_por_modelo_crud)
from app.schemas.Seguridad.Usuarios import UsuarioCreate, UsuarioUpdate, UsuarioResponse, LoginSchema, OTPVerifySchema, UsuarioAuthResponse, ResendOTPRequest
from app.models.Seguridad.Usuarios import Usuario
from app.models.Personas.personas import Persona
from app.utils.security import create_access_token
from app.utils.email_utils import enviar_email
from app.utils.utils import extraer_campo_foreign_key, extraer_campo_null
from typing import List
import logging
import pyotp

# Configurar logging
logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)

router = APIRouter()

#  Ruta para obtener todas las personas (SÍNCRONA)
@router.get("/usuarios/", response_model=List[UsuarioAuthResponse])
async def obtener_todos_los_usuarios(db: AsyncSession = Depends(get_async_db)):
    result = await db.execute(select(Usuario))  #  Obtiene `remember_token`
    usuarios = result.scalars().all()
    return [UsuarioResponse.model_validate(user) for user in usuarios]


# Endpoint para insertar un nuevo usuario (ASÍNCRONO)
@router.post("/usuarios/", response_model=UsuarioResponse)
async def crear_usuario(usuario: UsuarioCreate, db: AsyncSession = Depends(get_async_db)):
    try:
        usuario_creado = await insertar_usuario(db, usuario)
        return usuario_creado  #  Devuelve `UsuarioResponse`
    except Exception as e:
        error_message = str(e.orig) if hasattr(e, 'orig') else str(e)
        logger.error(f"Error al insertar usuario: {error_message}")
        raise HTTPException(status_code=400, detail=error_message)


    except IntegrityError as e:
        error_msg = str(e.orig).lower()
        logger.error(f"🔍 Error SQL en inserción de usuario: {error_msg}")

        if "foreign key" in error_msg:
            campo = extraer_campo_foreign_key(error_msg)
            raise HTTPException(status_code=400, detail=f"El valor del campo '{campo}' no es válido o no existe.")

        if "null value" in error_msg:
            campo = extraer_campo_null(error_msg)
            raise HTTPException(status_code=400, detail=f"El campo obligatorio '{campo}' no puede ser nulo.")

        if "duplicate key" in error_msg or "users_username_key" in error_msg or "violates unique constraint" in error_msg:
            raise HTTPException(status_code=400, detail="El nombre de usuario ya está en uso.")

        raise HTTPException(status_code=400, detail="Error de integridad en la base de datos.")

    except HTTPException as e:
        raise e

    except Exception as e:
        logger.error(f"Error inesperado al insertar usuario: {str(e)}")
        raise HTTPException(status_code=500, detail="Ocurrió un error inesperado al crear el usuario.")


# Endpoint para actualizar un usuario (ASÍNCRONO)
@router.put("/usuarios/{id}", response_model=dict)
async def modificar_usuario(id: int, usuario: UsuarioUpdate, db: AsyncSession = Depends(get_async_db)):
    try:
        response = await actualizar_usuario(db, id, usuario.dict(exclude_unset=True))
        return response

    except IntegrityError as e:
        error_msg = str(e.orig).lower()

        # Mostrar el error exacto en consola
        logger.error(f"Error SQL detectado: {repr(e)}")
        logger.error(f" Error no reconocido: {type(e.orig)}: {e.orig}")

        if "foreign key" in error_msg:
            campo = extraer_campo_foreign_key(error_msg)
            raise HTTPException(status_code=400, detail=f"El valor del campo '{campo}' no es válido o no existe.")

        if "null value" in error_msg:
            campo = extraer_campo_null(error_msg)
            raise HTTPException(status_code=400, detail=f"El campo obligatorio '{campo}' no puede ser nulo.")

        if "users_username_key" in error_msg or "duplicate key" in error_msg:
            raise HTTPException(status_code=400, detail="El nombre de usuario ya está en uso.")

        raise HTTPException(status_code=400, detail="Error de integridad en la base de datos.")

    except HTTPException as e:
        raise e

    except Exception as e:
        logger.error(f"Error al actualizar usuario {id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Error inesperado al actualizar el usuario.")


#  Endpoint para eliminar un usuario (ASÍNCRONO)
@router.delete("/usuarios/{id}", response_model=dict)
async def borrar_usuario(id: int, db: AsyncSession = Depends(get_async_db)):
    usuario_eliminado = await eliminar_usuario(db, id)
    if usuario_eliminado is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    return {"message": f"Usuario con ID {id} eliminado correctamente"}


#  Endpoint para obtener un usuario por ID (ASÍNCRONO)
@router.get("/usuarios/{id}", response_model=UsuarioResponse)
async def obtener_usuario(id: int, db: AsyncSession = Depends(get_async_db)):
    usuario = await obtener_usuario_por_id(db, id)
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return UsuarioResponse.model_validate(usuario)

#  Endpoint para iniciar sesión y obtener un token de acceso (ASÍNCRONO)
@router.post("/login")
async def login(login: LoginSchema, db: AsyncSession = Depends(get_async_db)):

    user = await autenticar_usuario(db, login.username, login.password)

    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Credenciales inválidas")

    # Generar código OTP y actualizar en la base de datos
    otp_response = await generar_otp(db, login.username)

    # Consultar los roles del usuario
    roles = await consultar_roles_por_modelo_crud(db, "User", user.id)
    role_names = [r["name"] for r in roles]

    #Consultar permisos
    permisos = await consultar_permisos_por_modelo_crud(db, "User", user.id)

    # Generar token con roles (opcional, si tu JWT los usa)
    access_token = create_access_token({
        "sub": user.username,
        "roles": role_names
    })

    return {
        "message": "Se ha enviado un código OTP a tu correo electrónico. Ingrese el código para completar el login.",
        "otp_expires_in": 120,
        "user": {
            "id": user.id,
            "username": user.username,
            "roles": role_names,
            "permissions": permisos
        },
        "access_token": access_token,
        "token_type": "bearer"
    }


#  Endpoint para verificar OTP (ASÍNCRONO)
@router.post("/verify-otp")
async def verify_otp(data: OTPVerifySchema, db: AsyncSession = Depends(get_async_db)):
    # Verificar código OTP
    otp_valid = await verificar_otp(db, data.username, data.otp_code)

    if not otp_valid:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Código OTP inválido o expirado")

    # Obtener el usuario
    user = await obtener_usuario_por_username(db, data.username)  # Debes tener esta función
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")


    # Obtener roles
    roles = await consultar_roles_por_modelo_crud(db, "User", user.id)
    role_names = [r["name"] for r in roles]

    # Obtener permisos
    permisos = await consultar_permisos_por_modelo_crud(db, "User", user.id)
    permiso_names = [p["name"] for p in permisos]

    # Generar token JWT
    access_token = create_access_token(data={"sub": user.username, "roles": role_names})

    # Devolver todo al frontend
    return {
        "message": "Autenticación exitosa",
        "access_token": access_token,
        "token_type": "bearer",
        "user": {
            "id": user.id,
            "username": user.username,
            "roles": role_names,
            "permissions": permiso_names
        }
    }


@router.post("/resend-otp")
async def resend_otp(data: ResendOTPRequest, db: AsyncSession = Depends(get_async_db)):
    user = await obtener_email_por_usuario(db, data.username)  #  Reutilizamos la misma función

    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    # Obtener el correo de la tabla `personas`
    persona = await db.get(Persona, user.cod_persona)

    if not persona or not persona.correo:
        raise HTTPException(status_code=400, detail="No se encontró el correo electrónico del usuario")

    email = persona.correo

    #  Si el usuario no tiene un OTP secreto, generarlo y guardarlo
    if not user.otp_secret:
        user.otp_secret = pyotp.random_base32()
        await db.commit()

    #  Generar código OTP con el secreto del usuario
    totp = pyotp.TOTP(user.otp_secret, interval=120)
    otp_code = totp.now()

    #  Enviar OTP por correo
    success = enviar_email(email, otp_code)

    if success:
        return {"message": "Código OTP enviado correctamente"}
    
    raise HTTPException(status_code=500, detail="Error al enviar el correo")
