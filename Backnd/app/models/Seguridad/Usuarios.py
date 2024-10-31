from sqlalchemy import Column, Integer, String, Date, DECIMAL, ForeignKey, CHAR, Boolean
from sqlalchemy.orm import relationship
from ...database import Base

class Usuario(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    cod_persona = Column(Integer, ForeignKey("tbl_personas.cod_persona"))
    nombre = Column(String(255), nullable=True)
    password = Column(String(255), nullable=True)
    remember_token = Column(String(100), nullable=True)
    username = Column(String(255), nullable=True)
    preguntas_contestadas = Column(Integer, nullable=True)
    estado = Column(Integer, nullable=True)
    primera_vez = Column(Boolean, nullable=True)
    fecha_vencimiento = Column(Date, nullable=False)
    intentos_preguntas = Column(Integer, nullable=False)
    preguntas_correctas = Column(Integer, nullable=False)