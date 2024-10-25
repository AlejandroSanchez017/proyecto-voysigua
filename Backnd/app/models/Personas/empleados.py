from sqlalchemy import Column, Integer, String, Date, DECIMAL, ForeignKey, CHAR
from sqlalchemy.orm import relationship
from ...database import Base

class Empleado(Base):
    __tablename__ = "tbl_empleado"

    cod_empleado = Column(Integer, primary_key=True, index=True)
    cod_persona = Column(Integer, ForeignKey("tbl_personas.cod_persona"))
    cod_tipo_empleado = Column(Integer, ForeignKey("tbl_tipo_empleado.cod_tipo_empleado"))
    cod_area = Column(Integer, ForeignKey("tbl_areas.cod_area"))
    cod_tipo_contrato = Column(Integer, ForeignKey("tbl_tipo_contrato.cod_tipo_contrato"))
    fecha_salida = Column(Date, nullable=True)
    motivo_salida = Column(String(500), nullable=True)
    fecha_contratacion = Column(Date, nullable=False)
    salario = Column(DECIMAL(10, 2), nullable=False)
    estado_empleado = Column(CHAR(1), nullable=False)
