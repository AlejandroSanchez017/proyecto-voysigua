from pydantic import BaseModel, Field
from typing import Optional

class TipoTelefonoBase(BaseModel):
    nombre_tipo_telefono: str

class TipoTelefonoCreate(TipoTelefonoBase):
    pass

class TipoTelefonoUpdate(TipoTelefonoBase):
    pass

class TipoTelefonoResponse(TipoTelefonoBase):
    cod_tipo_telefono: int

    class Config:
        from_attributes = True

class TelefonoBase(BaseModel):
    cod_persona: int = Field(..., description="Código de la persona propietaria del teléfono")
    telefono_principal: str = Field(..., min_length=4, max_length=15, description="Número principal del teléfono")
    exten: Optional[int] = Field(None, description="Extensión del teléfono (opcional)")
    codigo_area: int = Field(..., description="Código de área del teléfono")
    cod_tipo_telefono: int = Field(..., description="Código del tipo de teléfono (Ej: móvil, oficina)")
    estado: str = Field(..., pattern="^(A|I)$", description="Estado del teléfono (A=Activo, I=Inactivo)")

class TelefonoCreate(TelefonoBase):
    pass

class TelefonoUpdate(BaseModel):
    telefono_principal: str = Field(..., min_length=4, max_length=15, description="Número principal del teléfono")
    exten: Optional[int] = Field(None, description="Extensión telefónica (opcional)")
    codigo_area: int = Field(..., description="Código de área")
    cod_tipo_telefono: int = Field(..., description="Tipo de teléfono")
    estado: str = Field(..., pattern="^(A|I)$", description="Estado del teléfono")

class TelefonoResponse(TelefonoBase):
    cod_telefono: int

    class Config:
        from_attributes = True