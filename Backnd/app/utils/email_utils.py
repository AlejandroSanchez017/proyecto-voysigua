import smtplib
from email.message import EmailMessage

EMAIL_HOST = "smtp.gmail.com"
EMAIL_PORT = 587
EMAIL_USER = "voysigua76@gmail.com"
EMAIL_PASS = "bacd qmeg suie wupt"

def enviar_email(email, otp_code):
    """Envía un correo con el código OTP al usuario"""

    # 🔹 Validar que el email es un string válido antes de enviarlo
    if not isinstance(email, str) or "@" not in email:
        print(f"❌ [DEBUG] Error: Email inválido detectado: {email}")  # Depuración
        return False

    msg = EmailMessage()
    msg["Subject"] = "Tu código OTP de autenticación"
    msg["From"] = EMAIL_USER
    msg["To"] = email
    msg.set_content(f"Tu código de verificación es: {otp_code}\nEste código expira en 30 segundos.", charset="utf-8")

    try:
        with smtplib.SMTP(EMAIL_HOST, EMAIL_PORT) as server:
            server.starttls()
            server.login(EMAIL_USER, EMAIL_PASS)
            server.send_message(msg)
        print(f"✅ [DEBUG] Código OTP enviado correctamente a {email}")
        return True
    except Exception as e:
        print(f"❌ [DEBUG] Error al enviar OTP: {str(e)}")  # Depuración
        return False
