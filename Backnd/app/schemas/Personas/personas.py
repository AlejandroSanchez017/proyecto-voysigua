from pydantic import BaseModel, Field, EmailStr
from datetime import date
from typing import Optional

class PersonaBase(BaseModel):
    primer_nombre: str = Field(..., min_length=1, max_length=50, description="Primer nombre de la persona")
    apellido: Optional[str] = Field(None, min_length=1, max_length=50, description="Apellido de la persona")
    fecha_nacimiento: date = Field(..., description="Fecha de nacimiento en formato YYYY-MM-DD")
    dni: str = Field(..., min_length=8, max_length=20, description="Documento de identidad (DNI)")
    sexo: str = Field(..., pattern="^(M|F)$", description="Sexo de la persona (M/F)")
    correo: EmailStr = Field(..., description="Correo electrónico válido")
    estado: str = Field(..., pattern="^(A|I)$", description="Estado de la persona (A=Activo, I=Inactivo)")
    cod_tipo_persona: int = Field(..., description="Código del tipo de persona")

class PersonaCreate(PersonaBase):
    pass

class PersonaUpdate(BaseModel):
    primer_nombre: Optional[str] = Field(None, min_length=1, max_length=50)
    apellido: Optional[str] = Field(None, min_length=1, max_length=50)
    fecha_nacimiento: Optional[date] = None
    dni: Optional[str] = Field(None, min_length=8, max_length=20)
    sexo: Optional[str] = Field(None, pattern="^(M|F)$")
    correo: Optional[EmailStr] = None
    estado: Optional[str] = Field(None, pattern="^(A|I)$")
    cod_tipo_persona: Optional[int] = None

class PersonaResponse(PersonaBase):
    cod_persona: int
    class Config:
        from_attributes = True  

class TipoPersonaBase(BaseModel):
    tipo_persona: str = Field(..., min_length=2, max_length=50, description="Tipo de persona (Ej: Cliente, Empleado, etc.)")

class TipoPersonaCreate(TipoPersonaBase):
    pass

class TipoPersona(TipoPersonaBase):
    cod_tipo_persona: int
    class Config:
        from_attributes = True