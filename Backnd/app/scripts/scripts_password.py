import asyncpg
import os
from passlib.context import CryptContext
from dotenv import load_dotenv
from fastapi import HTTPException
import asyncio

# 📌 Cargar variables de entorno desde el archivo .env
load_dotenv()

# 🔧 Configuración segura de la base de datos usando variables de entorno
DB_CONFIG = {
    'database': os.getenv('DB_NAME'),
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD'),
    'host': os.getenv('DB_HOST'),
    'port': int(os.getenv('DB_PORT', 5432))  # Asegura que el puerto sea un número entero
}

# 🔑 Inicializar Passlib para usar bcrypt
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# 🔄 Función asíncrona para actualizar contraseñas en la base de datos
async def actualizar_contrasenas():
    """Actualiza las contraseñas en la base de datos si no están encriptadas"""
    try:
        conn = await asyncpg.connect(**DB_CONFIG)
        async with conn.transaction():
            # Obtener todas las contraseñas
            users = await conn.fetch("SELECT id, password FROM users;")

            for user in users:
                user_id, plain_password = user["id"], user["password"]
                
                if not plain_password.startswith("$2b$"):  # Si no está encriptada
                    hashed_password = pwd_context.hash(plain_password)
                    await conn.execute("UPDATE users SET password = $1 WHERE id = $2;", hashed_password, user_id)
                    print(f"🔑 Contraseña del usuario {user_id} actualizada.")

        await conn.close()
        print("✅ Todas las contraseñas han sido encriptadas correctamente.")

    except Exception as e:
        print(f"⚠️ Error al conectar o actualizar la base de datos: {e}")

# 🔐 Función asíncrona para iniciar sesión
async def login_user(username: str, password: str):
    """Verifica credenciales y autentica al usuario"""
    try:
        conn = await asyncpg.connect(**DB_CONFIG)
        result = await conn.fetchrow("SELECT password FROM users WHERE username = $1;", username)

        if result:
            hashed_password = result["password"]
            if pwd_context.verify(password, hashed_password):
                print("✅ Inicio de sesión exitoso.")
            else:
                raise HTTPException(status_code=400, detail="❌ Contraseña incorrecta.")
        else:
            raise HTTPException(status_code=404, detail="❌ Usuario no encontrado.")

        await conn.close()

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"⚠️ Error al iniciar sesión: {e}")

# 📌 Ejecutar la actualización de contraseñas si el script se ejecuta directamente
if __name__ == "__main__":
    asyncio.run(actualizar_contrasenas())