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

class EmpleadoUpdateBase(BaseModel):
    cod_persona: int
    cod_tipo_empleado: int
    cod_area: int
    cod_tipo_contrato: int
    fecha_salida: Optional[date] = None
    motivo_salida: Optional[str] = None
    fecha_contratacion: date
    salario: float
    estado_empleado: str


class EmpleadoDespedirBase(BaseModel):
    fecha_salida: date
    motivo_salida: str


# Esquema para crear empleado
class EmpleadoCreate(EmpleadoBase):
    pass

# Esquema para modificar empleado
class EmpleadoUpdate(EmpleadoUpdateBase):
    pass

# Esquema para despedir empleado
class EmpleadoDespedir(EmpleadoDespedirBase):
    fecha_salida: Optional [date]
    motivo_salida: Optional[str]

class Empleado(EmpleadoBase):
    cod_persona: int

    class Config:
        from_attributes = True

#-----------------------------------------------------------
class NombreTipoEmpleadoBase(BaseModel):
    nombre_tipo_empleado: str

#Esquema para crear Tipo Empleado
class NombreTipoEmpleadoCreate(NombreTipoEmpleadoBase):
    pass

class NombreTipoEmpleado(NombreTipoEmpleadoBase):
    cod_tipo_empleado: int

    class Config:
        from_attributes = True

#------------------------------------------------------------
class AreasBase(BaseModel):
    nombre_area: str

#Esquema para crea area
class AreasCreate(AreasBase):
    pass 

class Areas(AreasBase):
    cod_area: int

    class Config:
        from_attributes = True
#------------------------------------------------------------
class TipoContratoBase(BaseModel):
    tipo_contrato: str

#Esquema para crear Tipo Contrato
class TipoContratoCreate(TipoContratoBase):
    pass

class TipoContrato(TipoContratoBase):
    cod_tipo_contrato: int

    class Config:
        from_attributes = True