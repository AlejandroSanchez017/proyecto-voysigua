from sqlalchemy import Column, Integer, String, Date, ForeignKey, Boolean
from ...database import Base

class Usuario(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    cod_persona = Column(Integer, ForeignKey("tbl_personas.cod_persona"), nullable=False)
    nombre = Column(String(255), nullable=False)
    password = Column(String(255), nullable=False)  # Guardar encriptada
    remember_token = Column(String(512), nullable=True)  # Para recordar sesión
    username = Column(String(255), unique=True, nullable=False)  # Usuario único
    preguntas_contestadas = Column(Integer, default=0, nullable=False)
    estado = Column(Integer, default=1, nullable=False)  # 1 = Activo, 0 = Inactivo
    primera_vez = Column(Boolean, default=True, nullable=False)
    fecha_vencimiento = Column(Date, nullable=False)
    intentos_preguntas = Column(Integer, default=0, nullable=False)
    preguntas_correctas = Column(Integer, default=0, nullable=False)
