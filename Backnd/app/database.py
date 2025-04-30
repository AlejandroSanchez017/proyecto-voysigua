import os
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import create_engine
from dotenv import load_dotenv

# Cargar variables desde .env (solo tiene efecto localmente)
load_dotenv()

# Obtener DATABASE_URL (Render lo provee directamente)
DATABASE_URL_ASYNC = os.getenv("DATABASE_URL")

# Si no está definida (ej. en local), construirla desde partes
if not DATABASE_URL_ASYNC:
    DATABASE_URL_ASYNC = (
        f"postgresql+asyncpg://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}"
        f"@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
    )

# Derivar URL síncrona para psycopg2
DATABASE_URL_SYNC = DATABASE_URL_ASYNC.replace("asyncpg", "psycopg2")

# Depuración (puedes quitar esto en producción)
print(f"DATABASE_URL_ASYNC: {DATABASE_URL_ASYNC}")
print(f"DATABASE_URL_SYNC: {DATABASE_URL_SYNC}")

# Crear motores
async_engine = create_async_engine(DATABASE_URL_ASYNC, echo=False)
sync_engine = create_engine(DATABASE_URL_SYNC, echo=False)

# Sesión asíncrona
AsyncSessionLocal = sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    expire_on_commit=False
)

# Sesión síncrona
SyncSessionLocal = sessionmaker(
    bind=sync_engine,
    autocommit=False,
    autoflush=False,
)

# Declarative base para modelos
Base = declarative_base()

# Dependencia para FastAPI (async)
async def get_async_db():
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()

# Dependencia para FastAPI (sync)
def get_sync_db():
    db = SyncSessionLocal()
    try:
        yield db
    finally:
        db.close()
