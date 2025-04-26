from pydantic import BaseModel, Field
from typing import Optional

class SesionCreate(BaseModel):
    id: str = Field(..., max_length=255)
    user_id: int
    ip_address: Optional[str] = None
    user_agent: Optional[str] = None
    payload: Optional[str] = None
    last_activity: float  # timestamp UNIX como número

class SesionResponse(BaseModel):
    id: str
    user_id: int
    ip_address: Optional[str]
    user_agent: Optional[str]
    payload: Optional[str]
    last_activity: float

    class Config:
        from_attributes = True



class SesionUsuarioResponse(BaseModel):
    id: str
    ip_address: Optional[str]
    user_agent: Optional[str]
    last_activity: float

    class Config:
        from_attributes = True


class SesionInactivaResponse(BaseModel):
    id: str
    user_id: int
    last_activity: float
    tiempo_inactividad: str  # texto como "3 días", "5 horas", etc.
