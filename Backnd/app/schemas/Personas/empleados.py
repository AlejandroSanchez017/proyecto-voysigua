from pydantic import BaseModel
from datetime import date
from typing import Optional

# Base de empleado
class EmpleadoBase(BaseModel):
    cod_persona: int
    cod_tipo_empleado: int
    cod_area: int
    cod_tipo_contrato: int
    fecha_contratacion: date
    salario: float
    estado_empleado: str

# Esquema para crear empleado
class EmpleadoCreate(EmpleadoBase):
    pass

# Esquema para actualizar empleado
class EmpleadoUpdate(EmpleadoBase):
    fecha_salida: Optional[date]
    motivo_salida: Optional[str]

class Empleado(EmpleadoBase):
    cod_persona: int

    class Config:
        orm_mode = True
