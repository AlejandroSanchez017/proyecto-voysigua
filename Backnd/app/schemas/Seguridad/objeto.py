from pydantic import BaseModel, Field
from typing import Literal, Optional

class ObjetoCreate(BaseModel):
    objeto: str = Field(..., min_length=1, max_length=255)
    descripcion: Optional[str] = None
    status: Literal['active', 'inactive'] = 'active'

    

class ObjetoResponse(BaseModel):
    id:int
    objeto: str = Field(..., min_length=1, max_length=255)
    descripcion: Optional[str] = None
    status: Literal['active', 'inactive'] = 'active'
    class Config:
        from_attributes = True


class ObjetoUpdate(BaseModel):
    objeto: Optional[str] = Field(None, max_length=255)
    descripcion: Optional[str] = None
    status: Optional[Literal['active', 'inactive']] = None

    class Config:
        from_attributes = True

class ObjetoResponse(BaseModel):
    id: int
    objeto: str
    descripcion: Optional[str] = None
    status: Literal['active', 'inactive']

    class Config:
        from_attributes = True

class ObjetoResponse(BaseModel):
    id: int
    objeto: str
    descripcion: Optional[str] = None
    status: Literal['active', 'inactive']

    class Config:
        from_attributes = True
