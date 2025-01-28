from pydantic import BaseModel
from datetime import date

class UsuarioBase(BaseModel):
    cod_persona: int
    nombre: str
    password: str
    remember_token: str
    username: str
    preguntas_contestadas: int
    estado: int
    primera_vez: bool
    fecha_vencimiento: date
    intentos_preguntas: int
    preguntas_correctas: int

class UsuarioCreate(UsuarioBase):
    pass

class UsuarioUpdate(UsuarioBase):
    pass # No se necesita agregar más atributos por ahora

class Usuario(UsuarioBase):
    id: int

    class Config:
        from_attributes = True