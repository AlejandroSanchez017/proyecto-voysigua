from pydantic import BaseModel
from typing import Optional
from datetime import date, time

class MandadoBase(BaseModel):
    cod_persona: int
    tipo_pago_id: int
    cod_tipo_mandado: int
    cod_estado_mandado: int
    cuadre_motorista_id: int
    fecha: date
    cliente: str
    descripcion: str
    detalles: Optional[str] = None
    total: float
    costo_base: float
    costo_extra: float
    hora_inicio: time
    hora_fin: time

class MandadoCreate(MandadoBase):
    pass

class MandadoUpdate(MandadoBase):
    cod_mandado: int

class MandadoEliminar(BaseModel):
    cod_mandado: int


class MandadoResponse(BaseModel):
    cod_mandado: int
    cod_cliente: int
    cod_motorista: int
    cod_estado: int
    cod_tipo_pago: int
    fecha: date
    persona_recibe: str
    direccion_entrega: str
    observaciones: Optional[str]
    costo_total: float
    abono: float
    saldo: float
    hora: time

    class Config:
        orm_mode = True 