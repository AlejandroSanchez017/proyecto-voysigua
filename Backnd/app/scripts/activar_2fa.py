import sys
import os
import pyotp
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.database import async_session_maker
from app.models.Seguridad.Usuarios import Usuario

# Agregar la carpeta raíz del proyecto al `sys.path`
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

async def activar_2fa(db: AsyncSession, username: str):
    result = await db.execute(select(Usuario).filter(Usuario.username == username))
    user = result.scalars().first()

    if not user:
        print("❌ Usuario no encontrado")
        return

    if user.otp_secret:
        print(f"🔹 El usuario {username} ya tiene 2FA activado.")
        return

    # 🔥 Generar un nuevo `otp_secret`
    user.otp_secret = pyotp.random_base32()

    await db.commit()
    await db.refresh(user)
    print(f"✅ 2FA activado para {username}, Secreto OTP: {user.otp_secret}")

async def main():
    async with async_session_maker() as db:
        username = input("Ingrese el username del usuario para activar 2FA: ")
        await activar_2fa(db, username)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())