from pydantic import BaseModel
from typing import Optional

class RoleCreate(BaseModel):
    name: str
    guard_name: Optional[str] = None
    status: str  # 'active' o 'inactive'

class RoleResponse(BaseModel):
    id: int
    name: str
    guard_name: Optional[str] = None
    status: str

    class Config:
        from_attributes = True

class RoleUpdate(BaseModel):
    name: str
    guard_name: Optional[str] = None
    status: str