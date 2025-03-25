from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from ...schemas.Seguridad.Usuarios import LoginSchema, OTPVerifySchema
from ...models.Seguridad.Usuarios import Usuario
from ...utils.security import create_access_token
from sqlalchemy.sql import select
from ...crud.Seguridad.Usuarios import (
    autenticar_usuario, generar_otp, verificar_otp, obtener_email_por_usuario
)
from app.database import get_async_db, get_sync_db
from ...utils.email_utils import enviar_email

router = APIRouter()

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
    is_valid = await verificar_otp(db, data.username, data.otp_code)
    if is_valid:
        # Generar el token JWT
        access_token = create_access_token(data={"sub": data.username})

        # Guardar solo el `access_token` en la base de datos
        user_result = await db.execute(select(Usuario).filter(Usuario.username == data.username))
        user = user_result.scalars().first()
        
        if user:
            user.remember_token = str(access_token)
            await db.commit()
            await db.refresh(user)
        
        return {"access_token": access_token, "token_type": "bearer"}
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Código OTP inválido")
