from pydantic import BaseModel
from typing import Optional

class AssignPermissionToRole(BaseModel):
    permission_id: int
    role_id: int

class PermissionResponse(BaseModel):
    id: int
    name: str
    guard_name: Optional[str] = None

    class Config:
        from_attributes = True
        
class RoleResponse(BaseModel):
    id: int
    name: str
    status: Optional[str] = None

    class Config:
        from_attributes = True