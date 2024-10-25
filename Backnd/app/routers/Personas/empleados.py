from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ...crud.Personas.empleados import insertar_empleado, actualizar_empleado, despedir_empleado, eliminar_empleado, obtener_empleado_por_id, obtener_todos_los_empleados 
from ...schemas.Personas.empleados import EmpleadoCreate, EmpleadoUpdate, Empleado
from ...database import get_db


router = APIRouter()

@router.post("/empleados/")
def crear_empleado(empleado: EmpleadoCreate, db: Session = Depends(get_db)):
    try:
        insertar_empleado(db, empleado)
        return {"message": "Empleado insertado correctamente"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.put("/empleados/{cod_empleado}")
def modificar_empleado(cod_empleado: int, empleado: EmpleadoUpdate, db: Session = Depends(get_db)):
    try:
        actualizar_empleado(db, cod_empleado, empleado)
        return {"message": "Empleado actualizado correctamente"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.put("/empleados/despedir/{cod_empleado}")
def despedir_empleado(cod_empleado: int, fecha_salida: str, motivo_salida: str, db: Session = Depends(get_db)):
    try:
        despedir_empleado(db, cod_empleado, fecha_salida, motivo_salida)
        return {"message": "Empleado despedido correctamente"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/empleados/{cod_empleado}")
def eliminar_empleado(cod_empleado: int, db: Session = Depends(get_db)):
    try:
        eliminar_empleado(db, cod_empleado)
        return {"message": "Empleado eliminado correctamente"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@router.get("/empleados/{empleado_id}")
def obtener_empleado(empleado_id: int, db: Session = Depends(get_db)):
    empleado = obtener_empleado_por_id(db, empleado_id)
    return empleado

@router.get("/empleados/", response_model=list[Empleado])
def obtener_empleado (skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    empleados = obtener_todos_los_empleados(db, skip=skip, limit=limit)
    return empleados
