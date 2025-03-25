from pydantic import BaseModel
from typing import Optional

class PermisoCreate(BaseModel):
    name: str
    guard_name: Optional[str] = None

class PermisoUpdate(BaseModel):
    name: str
    guard_name: Optional[str] = None

class PermisoResponse(BaseModel):
    id: int
    name: str
    guard_name: Optional[str] = None

    class Config:
        from_attributes = True