from pydantic import BaseModel, Field
from datetime import date
from typing import Optional, Literal

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


class EmpleadoDespedir(BaseModel):
    fecha_salida: Optional[date] = None
    motivo_salida: Optional[str] = None


class EmpleadoCreate(EmpleadoBase):
    pass


class EmpleadoUpdate(EmpleadoUpdateBase):
    pass

class EmpleadoResponse(EmpleadoBase):
    cod_empleado: int

    # Sobrescribimos los campos que en EmpleadoBase son int,
    # para permitir que vengan como None si están NULL en la DB.
    cod_tipo_empleado: Optional[int] = None
    cod_area: Optional[int] = None
    cod_tipo_contrato: Optional[int] = None

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

class MarcaBase(BaseModel):
    nombre_marca: str

class MarcaCreate(MarcaBase):
    pass

class MarcaUpdate(MarcaBase):
    pass

class MarcaResponse(MarcaBase):
    cod_marca: int

    class Config:
        from_attributes = True

class TipoTransporteBase(BaseModel):
    nombre_tipo_transporte: str

class TipoTransporteCreate(TipoTransporteBase):
    pass

class TipoTransporteUpdate(TipoTransporteBase):
    pass

class TipoTransporteResponse(TipoTransporteBase):
    cod_tipo_transporte: int

    class Config:
        from_attributes = True

class VehiculoMotoristaBase(BaseModel):
    cod_persona: int = Field(..., description="ID del motorista (persona)")
    cod_tipo_transporte: int = Field(..., description="Tipo de transporte")
    modelo_transporte: str = Field(..., max_length=50)
    numero_placa: str = Field(..., max_length=20)
    chasis: str = Field(..., max_length=50)
    cod_marca: int = Field(..., description="Marca del vehículo")
    estado: Literal["A", "I"] = Field(..., description="Estado del vehículo (A/I)")

class VehiculoMotoristaCreate(VehiculoMotoristaBase):
    pass

class VehiculoMotoristaUpdate(BaseModel):
    cod_tipo_transporte: int
    modelo_transporte: str = Field(..., max_length=50)
    numero_placa: str = Field(..., max_length=20)
    chasis: str = Field(..., max_length=50)
    cod_marca: int
    estado: Literal["A", "I"]

class VehiculoMotoristaResponse(BaseModel):
    cod_vehiculo: int
    cod_persona: int
    cod_tipo_transporte: int
    modelo_transporte: str
    numero_placa: str
    chasis: str
    cod_marca: int
    estado: str

    class Config:
        from_attributes = True