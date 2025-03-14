from pydantic import BaseModel
from datetime import date
from typing import Optional


# ------------------------------------------------------------------------------
# BASES
# ------------------------------------------------------------------------------
# Estas clases “base” suelen usarse para la lógica de creación/actualización,
# por eso en EmpleadoBase los campos son todos obligatorios.
# Si *durante la creación* necesitas 'cod_area', 'cod_tipo_empleado' y 'cod_tipo_contrato',
# lo dejas como int (no Optional). Aun así, podrían ser Optional si te interesa
# que sean opcionales al crear.
class EmpleadoBase(BaseModel):
    cod_persona: int
    cod_tipo_empleado: int
    cod_area: int
    cod_tipo_contrato: int
    fecha_salida: Optional[date] = None
    motivo_salida: Optional[str] = None
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


# ------------------------------------------------------------------------------
# DESPEDIR
# ------------------------------------------------------------------------------
# Si *necesitas* que sean obligatorios, mantén fecha_salida y motivo_salida como no opcionales.
# De lo contrario, hazlos opcionales. Pero NO mezcles la definición duplicada dentro de la misma clase.
class EmpleadoDespedir(BaseModel):
    fecha_salida: Optional[date] = None
    motivo_salida: Optional[str] = None


# ------------------------------------------------------------------------------
# CREAR / MODIFICAR
# ------------------------------------------------------------------------------
# Hereda de las "bases" para creación y actualización.
class EmpleadoCreate(EmpleadoBase):
    pass


class EmpleadoUpdate(EmpleadoUpdateBase):
    pass


# ------------------------------------------------------------------------------
# RESPUESTA
# ------------------------------------------------------------------------------
# Aquí está el ajuste clave:
# - EmpleadoResponse hereda de EmpleadoBase, que tiene
#   cod_area, cod_tipo_empleado, cod_tipo_contrato como int obligatorios,
#   pero en la BD pueden ser NULL al despedir.
# - Para “sobrescribirlos” y permitir None, redeclaramos *solo* esos campos
#   como Optional[int].
class EmpleadoResponse(EmpleadoBase):
    cod_empleado: int

    # Sobrescribimos los campos que en EmpleadoBase son int,
    # para permitir que vengan como None si están NULL en la DB.
    cod_tipo_empleado: Optional[int] = None
    cod_area: Optional[int] = None
    cod_tipo_contrato: Optional[int] = None

    # Campos extra (relaciones) también opcionales
    nombre_tipo_empleado: Optional[str] = None
    nombre_area: Optional[str] = None
    tipo_contrato: Optional[str] = None

    class Config:
        from_attributes = True


# ------------------------------------------------------------------------------
# TIPOS AUXILIARES
# ------------------------------------------------------------------------------
class NombreTipoEmpleadoBase(BaseModel):
    nombre_tipo_empleado: str

class NombreTipoEmpleadoCreate(NombreTipoEmpleadoBase):
    pass

class NombreTipoEmpleado(NombreTipoEmpleadoBase):
    cod_tipo_empleado: int

    class Config:
        from_attributes = True

class AreasBase(BaseModel):
    nombre_area: str

class AreasCreate(AreasBase):
    pass 

class Areas(AreasBase):
    cod_area: int

    class Config:
        from_attributes = True

class TipoContratoBase(BaseModel):
    tipo_contrato: str

class TipoContratoCreate(TipoContratoBase):
    pass

class TipoContrato(TipoContratoBase):
    cod_tipo_contrato: int

    class Config:
        from_attributes = True