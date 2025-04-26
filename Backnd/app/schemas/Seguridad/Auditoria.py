from pydantic import BaseModel
from datetime import datetime

class AuditoriaResponse(BaseModel):
    idauditoria: int
    tipo: str
    tabla: str
    registro: int
    campo: str
    valorantes: str | None
    valordespues: str | None
    fecha: datetime
    usuario: str
    pc: str | None

    class Config:
        from_attributes = True

class AuditoriaResponse(BaseModel):
    idauditoria: int
    tipo: str
    tabla: str
    registro: int
    campo: str
    valorantes: str | None
    valordespues: str | None
    fecha: datetime
    usuario: str
    pc: str | None

    class Config:
        from_attributes = True
