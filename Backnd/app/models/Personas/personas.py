from sqlalchemy import Column, Integer, String, Date, CHAR, ForeignKey
from sqlalchemy.orm import relationship
from ...database import Base

class TipoPersona(Base):
    __tablename__ = 'tbl_tipo_persona'
    cod_tipo_persona = Column(Integer, primary_key=True, index=True)
    tipo_persona = Column(String(50), nullable=False, unique=True)

class Persona(Base):
    __tablename__ = 'tbl_personas'
    cod_persona = Column(Integer, primary_key=True, index=True)
    cod_tipo_persona = Column(Integer, ForeignKey('tbl_tipo_persona.cod_tipo_persona', ondelete='RESTRICT'), nullable=False)
    dni = Column(String(20), nullable=False, unique=True)
    primer_nombre = Column(String(50), nullable=False)
    apellido = Column(String(50), nullable=True)
    fecha_nacimiento = Column(CHAR(10), nullable=False)
    sexo = Column(CHAR(1), nullable=False)
    correo = Column(String(100), nullable=False, unique=True)
    estado = Column(CHAR(1), nullable=False)

    # Relación con TipoPersona
    tipo_persona = relationship("TipoPersona", back_populates="personas")

# Relación inversa en TipoPersona
TipoPersona.personas = relationship("Persona", back_populates="tipo_persona")