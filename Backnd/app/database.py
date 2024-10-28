from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Configura la URL de la base de datos PostgreSQL
DATABASE_URL = "postgresql://postgres:password@localhost:5432/VoySigua"

# Crea el motor de la base de datos
engine = create_engine(DATABASE_URL)

# Crea una sesión para interactuar con la base de datos
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Modelo base para las tablas
Base = declarative_base()

# Dependencia para obtener una sesión de la base de datos en cada solicitud
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
