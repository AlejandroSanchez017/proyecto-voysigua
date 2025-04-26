from sqlalchemy import Column, Integer, String, ForeignKey, CHAR
from app.database import Base

class TipoTelefono(Base):
    __tablename__ = "tbl_tipo_telefono"

    cod_tipo_telefono = Column(Integer, primary_key=True, index=True)
    nombre_tipo_telefono = Column(String(50), unique=True, nullable=False)

class Telefono(Base):
    __tablename__ = "tbl_telefonos"

    cod_telefono = Column(Integer, primary_key=True, index=True)
    cod_persona = Column(Integer, ForeignKey("tbl_personas.cod_persona", ondelete="CASCADE"), nullable=False)
    telefono_principal = Column(String(15), nullable=False)
    exten = Column(Integer, nullable=True)
    codigo_area = Column(Integer, nullable=False)
    cod_tipo_telefono = Column(Integer, ForeignKey("tbl_tipo_telefono.cod_tipo_telefono", ondelete="RESTRICT"), nullable=False)
    estado = Column(CHAR(1), nullable=False)