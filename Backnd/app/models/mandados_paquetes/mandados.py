from sqlalchemy import Column, Integer, String, Date, Time, Numeric, ForeignKey
from ...database import Base

class Mandado(Base):
    __tablename__ = "mandados"

    cod_mandado = Column(Integer, primary_key=True, index=True)
    cod_persona = Column(Integer, ForeignKey("tbl_personas.cod_persona"), nullable=False)
    tipo_pago_id = Column(Integer, ForeignKey("tipo_pago.id"), nullable=False)
    cod_tipo_mandado = Column(Integer, ForeignKey("tipo_mandado.id"), nullable=False)
    cod_estado_mandado = Column(Integer, ForeignKey("estado_mandado.id"), nullable=False)
    cuadre_motorista_id = Column(Integer, ForeignKey("cuadres_motorista.id"), nullable=False)

    fecha = Column(Date, nullable=False)
    cliente = Column(String(255), nullable=False)
    descripcion = Column(String(500), nullable=False)
    detalles = Column(String(1000), nullable=True)

    total = Column(Numeric, nullable=False)
    costo_base = Column(Numeric, nullable=False)
    costo_extra = Column(Numeric, nullable=False)

    hora_inicio = Column(Time, nullable=False)
    hora_fin = Column(Time, nullable=False)
