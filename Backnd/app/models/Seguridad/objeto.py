from sqlalchemy import Column, Integer, String, Text
from app.database import Base

class Objetos(Base):
    __tablename__ = "objetos"

    id = Column(Integer, primary_key=True, index=True)
    objeto = Column(String, nullable=False)
    descripcion = Column(Text)
    status = Column(String)