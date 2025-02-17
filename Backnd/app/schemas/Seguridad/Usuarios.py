from pydantic import BaseModel
from datetime import date
from typing import Optional

class UsuarioBase(BaseModel):
    cod_persona: int
    nombre: str
    password: str
    remember_token: Optional[str] = None
    username: str
    preguntas_contestadas: int
    estado: int
    primera_vez: bool
    fecha_vencimiento: date
    intentos_preguntas: int
    preguntas_correctas: int


# Para la creación de un usuario
class UsuarioCreate(BaseModel):
    cod_persona: int
    nombre: str
    password: str
    remember_token: Optional[str] = None
    username: str
    preguntas_contestadas: int
    estado: int
    primera_vez: bool
    fecha_vencimiento: date
    intentos_preguntas: int
    preguntas_correctas: int

# Para la autenticación (Login)
class UsuarioLogin(BaseModel):
    username: str
    password: str

# Para la respuesta (Sin exponer la contraseña)
class UsuarioResponse(BaseModel):
    id: int
    cod_persona: int
    nombre: str
    remember_token: Optional[str] = None
    username: str
    preguntas_contestadas: int
    estado: int
    primera_vez: bool
    fecha_vencimiento: date
    intentos_preguntas: int
    preguntas_correctas: int

    class Config:
        from_attributes = True  # Convierte SQLAlchemy a Pydantic



class UsuarioUpdate(BaseModel):
    cod_persona: Optional[int] = None
    nombre: Optional[str] = None
    password: Optional[str] = None  # ✅ Permitir que la contraseña sea opcional
    username: Optional[str] = None
    preguntas_contestadas: Optional[int] = None
    estado: Optional[int] = None
    primera_vez: Optional[bool] = None
    fecha_vencimiento: Optional[date] = None
    intentos_preguntas: Optional[int] = None
    preguntas_correctas: Optional[int] = None

class UsuarioSchema(UsuarioBase):
    id: int

    class Config:
        from_attributes = True 

class LoginSchema(BaseModel):
    username: str
    password: str