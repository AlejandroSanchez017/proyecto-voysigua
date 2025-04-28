from pydantic import BaseModel, Field
from typing import Optional

class DepartamentoBase(BaseModel):
    nombre_departamento: str

class DepartamentoCreate(DepartamentoBase):
    pass

class DepartamentoUpdate(DepartamentoBase):
    pass

class DepartamentoResponse(DepartamentoBase):
    cod_departamento: int

    class Config:
        from_atributes = True 

class CiudadBase(BaseModel):
    nombre_ciudad: str
    cod_departamento: int

class CiudadCreate(CiudadBase):
    pass

class CiudadUpdate(CiudadBase): 
    pass

class CiudadResponse(CiudadBase):
    cod_ciudad: int

    class Config:
        from_atributes = True

class TipoDireccionBase(BaseModel):
    nombre_tipo_direccion: str

class TipoDireccionCreate(TipoDireccionBase):
    pass

class TipoDireccionUpdate(TipoDireccionBase):
    pass

class TipoDireccionResponse(TipoDireccionBase):
    cod_tipo_direccion: int

    class Config:
        from_atributes = True

class DireccionBase(BaseModel):
    
    cod_ciudad: int = Field(..., description="ID de la ciudad")
    cod_tipo_direccion: int = Field(..., description="ID del tipo de dirección")
    direccion1: str = Field(..., max_length=255, description="Primera línea de dirección")
    direccion2: Optional[str] = Field(None, max_length=255, description="Segunda línea de dirección (opcional)")
    direccion3: Optional[str] = Field(None, max_length=255, description="Tercera línea de dirección (opcional)")
    estado_direccion: str = Field(..., pattern="^(A|I)$", description="Estado (A=Activo, I=Inactivo)")

class DireccionCreate(DireccionBase):
    pass

class DireccionUpdate(BaseModel):
    cod_tipo_direccion: int = Field(..., description="ID del tipo de dirección")
    direccion1: str = Field(..., max_length=255, description="Primera línea de dirección")
    direccion2: Optional[str] = Field(None, max_length=255)
    direccion3: Optional[str] = Field(None, max_length=255)
    estado_direccion: str = Field(..., pattern="^(A|I)$", description="Estado de la dirección (A/I)")

class DireccionResponse(DireccionBase):
    cod_direccion: int
    cod_persona: int 

    class Config:
        from_attributes = True