from sqlalchemy import Column, Integer, String, CHAR, TIMESTAMP
from app.database import Base

class Auditoria(Base):
    __tablename__ = "auditoria"

    idauditoria = Column(Integer, primary_key=True, index=True)
    tipo = Column(CHAR(1), nullable=False)
    tabla = Column(String(50), nullable=False)
    registro = Column(Integer, nullable=False)
    campo = Column(String(50), nullable=False)
    valorantes = Column(String(100))
    valordespues = Column(String(100))
    fecha = Column(TIMESTAMP, nullable=False)
    usuario = Column(String(50), nullable=False)
    pc = Column(String(50))

