from sqlalchemy import Column, Integer, String, Date, DECIMAL, ForeignKey, CHAR
from sqlalchemy.orm import relationship
from ...database import Base

class Areas(Base):
    __tablename__ = 'tbl_areas'
    cod_area= Column(Integer, primary_key=True, index=True)
    nombre_area = Column(String(50), nullable=False, unique=True)

class NombreTipoEmpleado(Base):
    __tablename__ = 'tbl_tipo_empleado'
    cod_tipo_empleado = Column(Integer, primary_key=True, index=True)
    nombre_tipo_empleado = Column(String(50), nullable=False, unique=True)

class TipoContrato(Base):
    __tablename__ = 'tbl_tipo_contrato'
    cod_tipo_contrato= Column(Integer, primary_key=True, index=True)
    tipo_contrato = Column(String(50), nullable=False, unique=True)


class Empleado(Base):
    __tablename__ = "tbl_empleado"

    cod_empleado = Column(Integer, primary_key=True, index=True)
    cod_persona = Column(Integer, ForeignKey("tbl_personas.cod_persona"))
    cod_tipo_empleado = Column(Integer, ForeignKey("tbl_tipo_empleado.cod_tipo_empleado"))
    cod_area = Column(Integer, ForeignKey("tbl_areas.cod_area"))
    cod_tipo_contrato = Column(Integer, ForeignKey("tbl_tipo_contrato.cod_tipo_contrato"))
    fecha_salida = Column(Date, nullable=True)
    motivo_salida = Column(String(500), nullable=True)
    fecha_contratacion = Column(Date, nullable=True)
    salario = Column(DECIMAL(10, 2), nullable=True)
    estado_empleado = Column(CHAR(1), nullable=True)

 # Relación con TipoEmpleado
    nombre_tipo_empleado = relationship("NombreTipoEmpleado", back_populates="empleado")

 # Relación con areas
    nombre_area = relationship("Areas", back_populates="empleado")

 # Relación con TipoContrato
    tipo_contrato= relationship("TipoContrato", back_populates="empleado")



# Relación inversa en TipoEmpleado
NombreTipoEmpleado.empleado = relationship("Empleado", back_populates="nombre_tipo_empleado")


# Relación inversa en areas
Areas.empleado = relationship("Empleado", back_populates="nombre_area")

# Relación inversa en TipoContrato
TipoContrato.empleado = relationship("Empleado", back_populates="tipo_contrato")