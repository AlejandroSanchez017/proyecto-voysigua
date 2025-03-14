from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from ...schemas.Seguridad.Usuarios import LoginSchema, OTPVerifySchema
from ...models.Seguridad.Usuarios import Usuario
from ...utils.security import create_access_token
from ...crud.Seguridad.Usuarios import autenticar_usuario, generar_otp, verificar_otp, obtener_email_por_usuario
from ...database import get_async_db
from ...utils.email_utils import enviar_email

router = APIRouter()

# ✅ Login de usuario (ASÍNCRONO)
@router.post("/login", response_model=dict)
async def login(login: LoginSchema, db: AsyncSession = Depends(get_async_db)):
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

# ✅ Verificar OTP y generar JWT (ASÍNCRONO)
@router.post("/verify-otp", response_model=dict)
async def verify_otp(data: OTPVerifySchema, db: AsyncSession = Depends(get_async_db)):
    is_valid_otp = await verificar_otp(db, data.username, data.otp_code)

    if not is_valid_otp:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Código OTP inválido")

    # Generar el token JWT
    access_token = create_access_token(data={"sub": data.username})

    # Guardar solo el `access_token` en la base de datos
    user = await db.get(Usuario, data.username)
    if user:
        user.remember_token = str(access_token)
        await db.commit()
        await db.refresh(user)

    return {"access_token": access_token, "token_type": "bearer"}
