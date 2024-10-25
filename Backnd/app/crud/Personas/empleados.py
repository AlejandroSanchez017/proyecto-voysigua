from sqlalchemy.orm import Session
from sqlalchemy.sql import text
from ...schemas.Personas.empleados import EmpleadoCreate, EmpleadoUpdate, Empleado
from ...models.Personas.empleados import Empleado

# Insertar empleado llamando a procedimiento almacenado
def insertar_empleado(db: Session, empleado: EmpleadoCreate):
    query = text("""
        CALL insertar_empleado(:cod_persona, :cod_tipo_empleado, :cod_area, :cod_tipo_contrato, 
                               :fecha_contratacion, :salario, :estado_empleado)
    """)
    db.execute(query, {
        "cod_persona": empleado.cod_persona,
        "cod_tipo_empleado": empleado.cod_tipo_empleado,
        "cod_area": empleado.cod_area,
        "cod_tipo_contrato": empleado.cod_tipo_contrato,
        "fecha_contratacion": empleado.fecha_contratacion,
        "salario": empleado.salario,
        "estado_empleado": empleado.estado_empleado
    })
    db.commit()

# Actualizar empleado
def actualizar_empleado(db: Session, cod_empleado: int, empleado: EmpleadoUpdate):
    query = text("""
        CALL actualizar_empleado(:cod_empleado, :cod_persona, :cod_tipo_empleado, :cod_area, 
                                 :cod_tipo_contrato, :fecha_contratacion, :salario, :estado_empleado)
    """)
    db.execute(query, {
        "cod_empleado": cod_empleado,
        "cod_persona": empleado.cod_persona,
        "cod_tipo_empleado": empleado.cod_tipo_empleado,
        "cod_area": empleado.cod_area,
        "cod_tipo_contrato": empleado.cod_tipo_contrato,
        "fecha_contratacion": empleado.fecha_contratacion,
        "salario": empleado.salario,
        "estado_empleado": empleado.estado_empleado
    })
    db.commit()

# Despedir empleado
def despedir_empleado(db: Session, cod_empleado: int, fecha_salida: str, motivo_salida: str):
    query = text("""
        CALL despedir_empleado(:cod_empleado, :fecha_salida, :motivo_salida)
    """)
    db.execute(query, {
        "cod_empleado": cod_empleado,
        "fecha_salida": fecha_salida,
        "motivo_salida": motivo_salida
    })
    db.commit()

# Eliminar empleado
def eliminar_empleado(db: Session, cod_empleado: int):
    query = text("""
        CALL eliminar_empleado(:cod_empleado)
    """)
    db.execute(query, {"cod_empleado": cod_empleado})
    db.commit()

# Obtener empleado por id
def obtener_empleado_por_id(db: Session, cod_empleado: int):
    return db.query(Empleado).filter(Empleado.cod_empleado == cod_empleado).first()

# Obtener todos los empleados
def obtener_todos_los_empleados(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Empleado).offset(skip).limit(limit).all()