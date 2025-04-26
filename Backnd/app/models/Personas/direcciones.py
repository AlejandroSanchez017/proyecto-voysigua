from sqlalchemy import Column, Integer, String, CHAR, ForeignKey
from app.database import Base
from sqlalchemy.orm import relationship

class Departamento(Base):
    __tablename__ = "tbl_departamentos"

    cod_departamento = Column(Integer, primary_key=True, index=True)
    nombre_departamento = Column(String(50), unique=True, nullable=False)

    ciudades = relationship("Ciudad", back_populates="departamento", cascade="all, delete")

class Ciudad(Base):
    __tablename__ = "tbl_ciudades"

    cod_ciudad = Column(Integer, primary_key=True, index=True)
    nombre_ciudad = Column(String(50), nullable=False, unique=True)
    cod_departamento = Column(Integer, ForeignKey("tbl_departamentos.cod_departamento", ondelete="CASCADE"), nullable=False)

    # Relación inversa con Departamento (si se define más adelante)
    departamento = relationship("Departamento", back_populates="ciudades")


class TipoDireccion(Base):
    __tablename__ = "tbl_tipo_direccion"

    cod_tipo_direccion = Column(Integer, primary_key=True, index=True)
    nombre_tipo_direccion = Column(String(50), nullable=False, unique=True)

class Direccion(Base):
    __tablename__ = "tbl_direcciones"

    cod_direccion = Column(Integer, primary_key=True, index=True)
    cod_persona = Column(Integer, ForeignKey("tbl_personas.cod_persona", ondelete="CASCADE"), nullable=False)
    cod_ciudad = Column(Integer, ForeignKey("tbl_ciudades.cod_ciudad", ondelete="CASCADE"), nullable=False)
    cod_tipo_direccion = Column(Integer, ForeignKey("tbl_tipo_direccion.cod_tipo_direccion", ondelete="RESTRICT"), nullable=False)

    direccion1 = Column(String(255), nullable=False)
    direccion2 = Column(String(255), nullable=True)
    direccion3 = Column(String(255), nullable=True)
    estado_direccion = Column(CHAR(1), nullable=False)