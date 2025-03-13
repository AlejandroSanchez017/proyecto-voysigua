from pydantic import BaseModel
from datetime import date
from typing import Optional

# Base para Usuario
class UsuarioBase(BaseModel):
    cod_persona: int
    nombre: str
    username: str
    estado: int
    primera_vez: bool
    fecha_vencimiento: date
    remember_token: Optional[str] = None

# Esquema para crear un usuario
class UsuarioCreate(UsuarioBase):
    password: str

# Esquema para la autenticación (Login)
class UsuarioLogin(BaseModel):
    username: str
    password: str

# Esquema de respuesta de usuario (sin exponer la contraseña)
class UsuarioResponse(UsuarioBase):
    id: int
    
    class Config:
        from_attributes = True  # Convierte SQLAlchemy a Pydantic

# Esquema para actualizar usuario (campos opcionales)
class UsuarioUpdate(BaseModel):
    cod_persona: Optional[int] = None
    nombre: Optional[str] = None
    password: Optional[str] = None  # Permitir que la contraseña sea opcional
    username: Optional[str] = None
    estado: Optional[int] = None
    primera_vez: Optional[bool] = None
    fecha_vencimiento: Optional[date] = None

# Esquema completo de usuario
class UsuarioSchema(UsuarioBase):
    id: int

    class Config:
        from_attributes = True 

# Esquema para el login
class LoginSchema(BaseModel):
    username: str
    password: str

# Esquema para verificación de OTP
class OTPVerifySchema(BaseModel):
    username: str
    otp_code: str