import psycopg2
from passlib.context import CryptContext
from fastapi import HTTPException

# Configuración para conectar a PostgreSQL
DB_CONFIG = {
    'dbname': 'VoySigua',
    'user': 'postgres',
    'password': '1234',
    'host': 'localhost',
    'port': 5432  # Puerto por defecto de PostgreSQL
}

# Inicializar Passlib para usar bcrypt
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Conectar a la base de datos
try:
    conn = psycopg2.connect(**DB_CONFIG)
    cursor = conn.cursor()

    # Obtener todas las contraseñas en texto plano (Asegúrate de que esto aplica en tu caso)
    cursor.execute("SELECT id, password FROM users;")  # Cambia 'usuario' por el nombre de tu tabla
    users = cursor.fetchall()

    for user_id, plain_password in users:
        if not plain_password.startswith("$2b$"):  # Si ya está encriptada, la ignoramos
            hashed_password = pwd_context.hash(plain_password)

            # Actualizar la contraseña en la base de datos
            cursor.execute("UPDATE users SET password = %s WHERE id = %s;", (hashed_password, user_id))
            print(f"Contraseña del usuario {user_id} actualizada.")

    # Confirmar los cambios
    conn.commit()
    print("Todas las contraseñas han sido encriptadas correctamente.")

except Exception as e:
    print(" Error al conectar o actualizar la base de datos:", e)

finally:
    if conn:
        cursor.close()
        conn.close()
# Función para iniciar sesión
def login_user(username: str, password: str):
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cursor = conn.cursor()

        # Obtener el usuario y la contraseña encriptada de la base de datos
        cursor.execute("SELECT password FROM usuario WHERE username = %s;", (username,))
        result = cursor.fetchone()

        if result:
            hashed_password = result[0]

            # Verificar si la contraseña ingresada coincide con la almacenada
            if pwd_context.verify(password, hashed_password):
                print("inicio de sesión exitoso.")
            else:
                raise HTTPException(status_code=400, detail="Contraseña incorrecta.")
        else:
            raise HTTPException(status_code=404, detail="Usuario no encontrado.")

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al iniciar sesión: {e}")

    finally:
        cursor.close()
        conn.close()