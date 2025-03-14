import os
import asyncio
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import create_engine  # ✅ Importamos `create_engine` para la sesión síncrona
from dotenv import load_dotenv

# Cargar variables desde el archivo .env
load_dotenv()

# Construir DATABASE_URL con variables de entorno
DATABASE_URL_ASYNC = f"postgresql+asyncpg://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
DATABASE_URL_SYNC = DATABASE_URL_ASYNC.replace("asyncpg", "psycopg2")  # ✅ Motor síncrono usa psycopg2

print(f"📌 DATABASE_URL_ASYNC: {DATABASE_URL_ASYNC}")  # Depuración
print(f"📌 DATABASE_URL_SYNC: {DATABASE_URL_SYNC}")  # Depuración

# ✅ Crear motores separados para asincronía y sincronía
async_engine = create_async_engine(DATABASE_URL_ASYNC, echo=False)
sync_engine = create_engine(DATABASE_URL_SYNC, echo=False)  # ✅ Motor síncrono

# ✅ Crear sesiones asíncronas
AsyncSessionLocal = sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    expire_on_commit=False
)

# ✅ Crear sesiones síncronas
SyncSessionLocal = sessionmaker(
    bind=sync_engine,  # ✅ Usamos `sync_engine` en lugar de `engine.sync_engine`
    autocommit=False,
    autoflush=False,
)

# ✅ Base para modelos
Base = declarative_base()

# ✅ Dependencia para obtener una sesión asíncrona
async def get_async_db():
    session = AsyncSessionLocal()
    try:
        yield session
    finally:
        await session.close()

# ✅ Dependencia para obtener una sesión síncrona
def get_sync_db():
    db = SyncSessionLocal()
    try:
        yield db
    finally:
        db.close()
