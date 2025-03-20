from pydantic import BaseModel, Field, EmailStr
from datetime import date
from typing import Optional, Union
import json

# Base para Usuario
class UsuarioBase(BaseModel):
    cod_persona: int = Field(..., description="Código de la persona asociada al usuario")
    nombre: str = Field(..., min_length=2, max_length=100, description="Nombre completo del usuario")
    username: str = Field(..., min_length=3, max_length=50, description="Nombre de usuario")
    estado: int = Field(..., description="Estado del usuario (Ejemplo: 1 = Activo, 0 = Inactivo)")
    primera_vez: bool = Field(..., description="Indica si el usuario es nuevo")
    fecha_vencimiento: date = Field(..., description="Fecha de expiración de la cuenta")

# Crear Usuario
class UsuarioCreate(UsuarioBase):
    password: str = Field(..., min_length=6, max_length=512, description="Contraseña del usuario (hash)")

# Actualizar Usuario
class UsuarioUpdate(BaseModel):
    cod_persona: Optional[int] = Field(None, description="Código de la persona asociada")
    nombre: Optional[str] = Field(None, min_length=2, max_length=100, description="Nombre completo")
    username: Optional[str] = Field(None, min_length=3, max_length=50, description="Nombre de usuario")
    password: Optional[str] = Field(None, min_length=6, max_length=512, description="Nueva contraseña del usuario")
    estado: Optional[int] = Field(None, description="Estado (1 = Activo, 0 = Inactivo)")
    primera_vez: Optional[bool] = Field(None, description="Indica si es la primera vez que inicia sesión")
    fecha_vencimiento: Optional[date] = Field(None, description="Fecha de expiración de la cuenta")

# Respuesta de Usuario (sin exponer la contraseña)
class UsuarioResponse(UsuarioBase):
    id: int
    otp_secret: Optional[str] = Field(None, description="Código secreto OTP del usuario (para 2FA)")

    class Config:
        from_attributes = True  # 🔹 Esto convierte un modelo SQLAlchemy a un esquema Pydantic

class UsuarioAuthResponse(UsuarioBase):
    id: int
    remember_token: Optional[str] = Field(None, description="Token de autenticación")
    otp_secret: Optional[str] = Field(None, description="Código secreto OTP del usuario (para 2FA)")

    class Config:
        from_attributes = True


# Esquema para login

class LoginSchema(BaseModel):
    username: str = Field(..., min_length=3, max_length=50, description="Nombre de usuario")
    password: str = Field(..., min_length=6, max_length=100, description="Contraseña del usuario")

# Esquema para verificación de OTP
class OTPVerifySchema(BaseModel):
    username: str = Field(..., min_length=3, max_length=50, description="Nombre de usuario")
    otp_code: str = Field(..., min_length=6, max_length=6, description="Código OTP de 6 dígitos")

class ResendOTPRequest(BaseModel):
    username: Optional[str] = None
    temp_token: Optional[str] = None
