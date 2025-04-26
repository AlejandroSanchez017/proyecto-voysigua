from sqlalchemy import Column, Integer, String, Text
from app.database import Base

class Parametro(Base):
    __tablename__ = "parametros"

    id = Column(Integer, primary_key=True, index=True)
    parametro = Column(String(255), nullable=False)
    valor = Column(Text, nullable=False)
    descripcion = Column(Text, nullable=True)
    estado = Column(String(20), default="activo", nullable=False)
    categoria = Column(String(100), nullable=True)
