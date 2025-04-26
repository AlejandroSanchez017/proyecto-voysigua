from sqlalchemy import Column, Integer, String, Date, DECIMAL, ForeignKey, CHAR
from sqlalchemy.orm import relationship
from app.database import Base

class Areas(Base):
    __tablename__ = 'tbl_areas'
    cod_area = Column(Integer, primary_key=True, index=True)
    nombre_area = Column(String(50), nullable=False, unique=True)

    empleados = relationship("Empleado", back_populates="area")  # ✅ Relación inversa correcta

class NombreTipoEmpleado(Base):
    __tablename__ = 'tbl_tipo_empleado'
    cod_tipo_empleado = Column(Integer, primary_key=True, index=True)
    nombre_tipo_empleado = Column(String(50), nullable=False, unique=True)

    empleados = relationship("Empleado", back_populates="tipo_empleado")  # ✅ Relación inversa correcta

class TipoContrato(Base):
    __tablename__ = 'tbl_tipo_contrato'
    cod_tipo_contrato = Column(Integer, primary_key=True, index=True)
    tipo_contrato = Column(String(50), nullable=False, unique=True)

    empleados = relationship("Empleado", back_populates="contrato")  # ✅ Relación inversa correcta

class Empleado(Base):
    __tablename__ = "tbl_empleado"

    cod_empleado = Column(Integer, primary_key=True, index=True)
    cod_persona = Column(Integer, ForeignKey("tbl_personas.cod_persona", ondelete="CASCADE"), nullable=False)
    cod_tipo_empleado = Column(Integer, ForeignKey("tbl_tipo_empleado.cod_tipo_empleado", ondelete="RESTRICT"), nullable=False)
    cod_area = Column(Integer, ForeignKey("tbl_areas.cod_area", ondelete="RESTRICT"), nullable=False)
    cod_tipo_contrato = Column(Integer, ForeignKey("tbl_tipo_contrato.cod_tipo_contrato", ondelete="RESTRICT"), nullable=False)
    fecha_salida = Column(Date, nullable=True)
    motivo_salida = Column(String(500), nullable=True)
    fecha_contratacion = Column(Date, nullable=False)
    salario = Column(DECIMAL(10, 2), nullable=False)
    estado_empleado = Column(CHAR(1), nullable=False)  # Debe ser 'A' o 'I'

    # ✅ Relaciones con tablas foráneas (corregido)
    tipo_empleado = relationship("NombreTipoEmpleado", back_populates="empleados", passive_deletes=True)
    area = relationship("Areas", back_populates="empleados", passive_deletes=True)
    contrato = relationship("TipoContrato", back_populates="empleados", passive_deletes=True)
