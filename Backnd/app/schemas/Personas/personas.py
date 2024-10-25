from pydantic import BaseModel
from datetime import date

class PersonaBase(BaseModel):
    primer_nombre: str
    apellido: str
    fecha_nacimiento: date
    sexo: str
    correo: str
    estado: str
    cod_tipo_persona: int

class PersonaCreate(PersonaBase):
    DNI: str

class PersonaUpdate(PersonaBase):
    pass # No se necesita agregar más atributos por ahora

class Persona(PersonaBase):
    cod_persona: int

    class Config:
        from_attributes = True