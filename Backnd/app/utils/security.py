import os
from jose import JWTError, jwt
from datetime import datetime, timedelta
from passlib.context import CryptContext
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from dotenv import load_dotenv

from ..models.Seguridad.Usuarios import Usuario
from ..schemas.Seguridad.usuarios import LoginSchema
from app.database import get_sync_db, get_async_db

# Cargar variables de entorno desde .env
load_dotenv()

# Configuración de autenticación
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")
SECRET_KEY = os.getenv("SECRET_KEY", "your_fallback_secret")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Configuración de hashing de contraseñas
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Función para generar el hash de una contraseña
def hash_password(password: str) -> str:
    return pwd_context.hash(password)

# Función para verificar contraseñas
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

# Función para generar un token de acceso
def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})

    token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return {"access_token": token, "token_type": "bearer"}

# Función asíncrona para autenticar usuario e iniciar sesión
async def authenticate_user(db: AsyncSession, login_data: LoginSchema):
    result = await db.execute(
        "SELECT id, username, password FROM usuarios WHERE username = :username",
        {"username": login_data.username}
    )
    user = result.fetchone()

    if not user or not verify_password(login_data.password, user.password):
        raise HTTPException(status_code=401, detail="Usuario o contraseña incorrectos")

    return user

# Función asíncrona para obtener el usuario actual a partir del token
async def get_current_user(db: AsyncSession = Depends(get_sync_db), token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=401,
        detail="No se pudieron validar las credenciales",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        exp = payload.get("exp")

        if username is None or exp is None:
            raise credentials_exception

        # Verificar si el token ha expirado
        if datetime.utcnow() > datetime.utcfromtimestamp(exp):
            raise HTTPException(status_code=401, detail="Token expirado")

        result = await db.execute(
            "SELECT id, username FROM usuarios WHERE username = :username",
            {"username": username}
        )
        user = result.fetchone()

        if user is None:
            raise credentials_exception

    except JWTError:
        raise credentials_exception

    return user