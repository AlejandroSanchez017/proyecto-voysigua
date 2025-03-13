import smtplib
import os
from email.message import EmailMessage
from dotenv import load_dotenv  # Cargar variables del .env

# Cargar variables de entorno
load_dotenv()

EMAIL_HOST = os.getenv("EMAIL_HOST", "smtp.gmail.com")
EMAIL_PORT = int(os.getenv("EMAIL_PORT", 587))
EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASS = os.getenv("EMAIL_PASS")

def enviar_email(email: str, otp_code: str):
    """Envía un correo con el código OTP al usuario"""

    # Validar que el email es un string válido antes de enviarlo
    if not isinstance(email, str) or "@" not in email:
        print(f"❌ [DEBUG] Error: Email inválido detectado: {email}")
        return False

    msg = EmailMessage()
    msg["Subject"] = "Tu código OTP de autenticación"
    msg["From"] = EMAIL_USER
    msg["To"] = email
    msg.set_content(f"Tu código de verificación es: {otp_code}\nEste código expira en 30 segundos.", charset="utf-8")

    try:
        with smtplib.SMTP(EMAIL_HOST, EMAIL_PORT) as server:
            server.starttls()  # Asegurar conexión segura
            server.login(EMAIL_USER, EMAIL_PASS)  # Iniciar sesión en el correo
            server.send_message(msg)  # Enviar email

        print(f"✅ [DEBUG] Código OTP enviado correctamente a {email}")
        return True

    except smtplib.SMTPAuthenticationError:
        print("❌ [ERROR] Fallo en la autenticación del servidor SMTP. Revisa EMAIL_USER y EMAIL_PASS.")
    except smtplib.SMTPException as e:
        print(f"❌ [ERROR] Error al enviar el correo: {str(e)}")
    return False