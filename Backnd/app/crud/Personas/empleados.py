from sqlalchemy.orm import Session
from sqlalchemy.sql import text
from ...schemas.Personas.empleados import EmpleadoCreate, EmpleadoUpdate, NombreTipoEmpleadoCreate, AreasCreate, TipoContratoCreate, EmpleadoDespedir
from ...models.Personas.empleados import Empleado, NombreTipoEmpleado, Areas, TipoContrato

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
                                 :cod_tipo_contrato, :fecha_salida, :motivo_salida, :fecha_contratacion, :salario, :estado_empleado)
    """)
    db.execute(query, {
        "cod_empleado": cod_empleado,
        "cod_persona": empleado.cod_persona,
        "cod_tipo_empleado": empleado.cod_tipo_empleado,
        "cod_area": empleado.cod_area,
        "cod_tipo_contrato": empleado.cod_tipo_contrato,
        "fecha_salida": empleado.fecha_salida,
        "motivo_salida": empleado.motivo_salida,
        "fecha_contratacion": empleado.fecha_contratacion,
        "salario": empleado.salario,
        "estado_empleado": empleado.estado_empleado
    })
    db.commit()

# Despedir empleado
def despedir_empleado(db: Session, cod_empleado: int, fecha_salida: str, motivo_salida: str):
    try:
        query = text("""
        CALL despedir_empleado(:cod_empleado, :fecha_salida, :motivo_salida)
        """)
        
        db.execute(query, {
            "cod_empleado": cod_empleado,
            "fecha_salida": fecha_salida,
            "motivo_salida": motivo_salida
        })
        db.commit()
        return {"message": f"Empleado con ID {cod_empleado} ha sido despedido exitosamente"}
    except Exception as e:
        db.rollback()
        raise Exception(f"Error al despedir empleado: {str(e)}")


# Eliminar empleado
def eliminar_empleado(db: Session, cod_empleado: int):
    db_empleado = db.query(Empleado).filter(Empleado.cod_empleado == cod_empleado).first()
    if db_empleado:
        db.delete(db_empleado)
        db.commit()
        return db_empleado
    return None

# Obtener empleado por id
def obtener_empleado_por_id(db: Session, cod_empleado: int):
    return db.query(Empleado).filter(Empleado.cod_empleado == cod_empleado).first()

# Obtener todos los empleados
def obtener_todos_los_empleados(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Empleado).offset(skip).limit(limit).all()

# Insertar TipoEmpleado
def insertar_tipo_empleado(db: Session, nombre_tipo_empleado: NombreTipoEmpleadoCreate):
    db_nombre_tipo_empleado = NombreTipoEmpleado(nombre_tipo_empleado=nombre_tipo_empleado.nombre_tipo_empleado)
    db.add(db_nombre_tipo_empleado)
    db.commit()
    db.refresh(db_nombre_tipo_empleado)  # Actualiza el objeto con los datos más recientes de la DB
    return db_nombre_tipo_empleado

# Eliminar TipoEmpleado
def eliminar_tipo_empleado(db: Session, cod_tipo_empleado: int):
    db_nombre_tipo_empleado = db.query(NombreTipoEmpleado).filter(NombreTipoEmpleado.cod_tipo_empleado == cod_tipo_empleado).first()
    if db_nombre_tipo_empleado:
        db.delete(db_nombre_tipo_empleado)
        db.commit()
        return db_nombre_tipo_empleado
    return None

#Insertar Area
def insertar_area(db: Session, nombre_area: AreasCreate):
    db_areas = Areas(nombre_area=nombre_area.nombre_area)
    db.add(db_areas)
    db.commit()
    db.refresh(db_areas)  # Actualiza el objeto con los datos más recientes de la DB
    return db_areas

# Eliminar TipoArea
def eliminar_area(db: Session, cod_area: int):
    db_areas = db.query(Areas).filter(Areas.cod_area == cod_area).first()
    if db_areas:
        db.delete(db_areas)
        db.commit()
        return db_areas
    return None

# Insertar TipoContrato
def insertar_tipo_contrato(db: Session, tipo_contrato: TipoContratoCreate):
    db_tipo_contrato = TipoContrato(tipo_contrato=tipo_contrato.tipo_contrato)
    db.add(db_tipo_contrato)
    db.commit()
    db.refresh(db_tipo_contrato)  # Actualiza el objeto con los datos más recientes de la DB
    return db_tipo_contrato

# Eliminar TipoContrato
def eliminar_tipo_contrato(db: Session, cod_tipo_contrato: int):
    db_tipo_contrato = db.query(TipoContrato).filter(TipoContrato.cod_tipo_contrato == cod_tipo_contrato).first()
    if db_tipo_contrato:
        db.delete(db_tipo_contrato)
        db.commit()
        return db_tipo_contrato
    return None