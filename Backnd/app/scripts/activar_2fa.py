import sys
import os
import pyotp
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models.Seguridad.Usuarios import Usuario

# Agregar la carpeta raíz del proyecto al `sys.path`
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

def activar_2fa(db: Session, username: str):
    user = db.query(Usuario).filter(Usuario.username == username).first()

    if not user:
        print("❌ Usuario no encontrado")
        return

    if user.otp_secret:
        print(f"🔹 El usuario {username} ya tiene 2FA activado.")
        return

    # 🔥 Generar un nuevo `otp_secret`
    user.otp_secret = pyotp.random_base32()
    
    db.commit()
    db.refresh(user)
    print(f"✅ 2FA activado para {username}, Secreto OTP: {user.otp_secret}")

if __name__ == "__main__":
    db = SessionLocal()
    username = input("Ingrese el username del usuario para activar 2FA: ")
    activar_2fa(db, username)
    db.close()
