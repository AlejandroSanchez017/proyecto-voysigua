from pydantic import BaseModel, Field
from typing import Optional, Literal

class ParametroCreate(BaseModel):
    parametro: str = Field(..., max_length=255)
    valor: str
    descripcion: Optional[str] = None
    categoria: Optional[str] = None
    estado: Literal['activo', 'inactivo'] = 'activo'
 


class ParametroUpdate(BaseModel):
    parametro: Optional[str] = Field(None, max_length=255)
    valor: Optional[str] = None
    descripcion: Optional[str] = None
    categoria: Optional[str] = None
    estado: Optional[Literal['activo', 'inactivo']] = None


class ParametroResponse(BaseModel):
    id: int
    parametro: str
    valor: str
    descripcion: Optional[str] = None
    estado: Literal['activo', 'inactivo']
    categoria: Optional[str] = None

    class Config:
        from_attributes = True