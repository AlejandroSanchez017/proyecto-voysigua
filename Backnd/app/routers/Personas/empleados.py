from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ...crud.Personas.empleados import insertar_empleado, actualizar_empleado, despedir_empleado, eliminar_empleado, obtener_empleado_por_id, obtener_todos_los_empleados, insertar_tipo_empleado, eliminar_tipo_empleado, insertar_area, eliminar_area 
from ...schemas.Personas.empleados import EmpleadoCreate, EmpleadoUpdate, Empleado, NombreTipoEmpleadoCreate, NombreTipoEmpleado, Areas, AreasCreate
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

@router.post("/tipo_empleado/")
def crear_tipo_empleado(nombre_tipo_empleado: NombreTipoEmpleadoCreate, db: Session = Depends(get_db)):
     try:
        insertar_tipo_empleado(db, nombre_tipo_empleado)
        return {"message": "Tipo empleado insertado correctamente"}
     except Exception as e:
        error_message = str(e.orig) if hasattr(e, 'orig') else str(e)
        raise HTTPException(status_code=400, detail=error_message)

# Ruta para eliminar un tipo_empleado por ID
@router.delete("/tipo_empleado/{cod_tipo_empleado}")
def borrar_tipo_empleado(cod_tipo_empleado: int, db: Session = Depends(get_db)):
    try:
        db_nombre_tipo_empleado = eliminar_tipo_empleado(db, cod_tipo_empleado)
        if db_nombre_tipo_empleado is None:
            raise HTTPException(status_code=404, detail="Tipo empleado no encontrado")
        return {"message": "Tipo empleado eliminado exitosamente"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

#Ruta Para Insertar Area
@router.post("/areas/")
def crear_area(nombre_area: AreasCreate, db: Session = Depends(get_db)):
     try:
        insertar_area(db, nombre_area)
        return {"message": "Area insertado correctamente"}
     except Exception as e:
        error_message = str(e.orig) if hasattr(e, 'orig') else str(e)
        raise HTTPException(status_code=400, detail=error_message)
    
# Ruta para eliminar un nombre area por ID
@router.delete("/areas/{cod_area}")
def borrar_area(cod_area: int, db: Session = Depends(get_db)):
    try:
        db_areas = eliminar_area(db, cod_area)
        if db_areas is None:
            raise HTTPException(status_code=404, detail="Tipo area no encontrado")
        return {"message": "Tipo area eliminada exitosamente"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    

