from sqlalchemy import Column, Integer, String, Date, CHAR, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base  # ✅ Importación absoluta

class TipoPersona(Base):
    __tablename__ = "tbl_tipo_persona"
    cod_tipo_persona = Column(Integer, primary_key=True, index=True)
    tipo_persona = Column(String(50), nullable=False, unique=True)

    # Relación con Persona
    personas = relationship("Persona", back_populates="tipo_persona_rel", cascade="all, delete-orphan")

class Persona(Base):
    __tablename__ = "tbl_personas"
    cod_persona = Column(Integer, primary_key=True, index=True)
    cod_tipo_persona = Column(
        Integer, ForeignKey("tbl_tipo_persona.cod_tipo_persona", ondelete="CASCADE"), nullable=False
    )
    dni = Column(String(20), nullable=False, unique=True)
    primer_nombre = Column(String(50), nullable=False)
    apellido = Column(String(50), nullable=True)
    fecha_nacimiento = Column(Date, nullable=False)
    sexo = Column(CHAR(1), nullable=False)
    correo = Column(String(100), nullable=False, unique=True)
    estado = Column(CHAR(1), nullable=False)

    # Relación con TipoPersona
    tipo_persona_rel = relationship("TipoPersona", back_populates="personas")

