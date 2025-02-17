from pydantic import BaseModel
from datetime import date
from typing import Optional

class PersonaBase(BaseModel):
    primer_nombre: str
    apellido: Optional[str]
    fecha_nacimiento: date
    dni: str
    sexo: str
    correo: str
    estado: str
    cod_tipo_persona: int


class PersonaCreate(PersonaBase):
    pass


class PersonaUpdate(PersonaBase):
    pass


class Persona(PersonaBase):
    cod_persona: int

    class Config:
        from_attributes = True  

class TipoPersonaBase(BaseModel):
    tipo_persona: str

class TipoPersonaCreate(TipoPersonaBase):
    pass

class TipoPersona(TipoPersonaBase):
    cod_tipo_persona: int

    class Config:
        from_attributes = True