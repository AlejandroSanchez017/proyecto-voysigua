from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import select
from app.database import get_async_db, get_sync_db  # ✅ Importamos ambas funciones correctamente
from app.models.Personas.empleados import Empleado as EmpleadoModel  # ✅ Corrección
from app.schemas.Personas.empleados import (
    EmpleadoCreate, EmpleadoResponse, NombreTipoEmpleadoCreate, TipoContrato,
    AreasCreate, TipoContratoCreate, EmpleadoDespedir, EmpleadoUpdate, NombreTipoEmpleado, Areas as AreasSchema
)
from app.crud.Personas.empleados import (
    insertar_empleado, actualizar_empleado, despedir_empleado_crud, eliminar_empleado, insertar_tipo_empleado, obtener_tipos_empleado, 
    eliminar_tipo_empleado, insertar_area, obtener_areas, eliminar_area, insertar_tipo_contrato, obtener_tipos_contrato,
    eliminar_tipo_contrato
)
from typing import List
import logging

logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)

router = APIRouter()

@router.post("/empleados/")
async def crear_empleado(empleado: EmpleadoCreate, db: AsyncSession = Depends(get_async_db)):
    try:
        await insertar_empleado(db, empleado)
        return {"message": "Empleado insertado correctamente"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.put("/empleados/{cod_empleado}")
async def modificar_empleado(cod_empleado: int, empleado: EmpleadoUpdate, db: AsyncSession = Depends(get_async_db)):
    try:
        await actualizar_empleado(db, cod_empleado, empleado)
        return {"message": "Empleado actualizado correctamente"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.put("/empleados/despedir/{cod_empleado}")
async def despedir_empleado(
    cod_empleado: int,
    datos: EmpleadoDespedir,
    db: AsyncSession = Depends(get_async_db)
):
    try:
        result = await despedir_empleado_crud(db, cod_empleado, datos)
        return result
    except Exception as e:
        error_message = str(e)
        logger.error(f"Error al despedir empleado {cod_empleado}: {error_message}")
        raise HTTPException(status_code=400, detail={"error": error_message})

@router.delete("/empleados/{cod_empleado}")
async def borrar_empleado(cod_empleado: int, db: AsyncSession = Depends(get_async_db)):
    try:
        db_empleado = await eliminar_empleado(db, cod_empleado)
        if db_empleado is None:
            raise HTTPException(status_code=404, detail="Empleado no encontrado")
        return {"message": "Empleado eliminado correctamente"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/empleados/", response_model=List[EmpleadoResponse])
def obtener_todos_los_empleados(db: Session = Depends(get_sync_db)):
    empleados = db.execute(
        select(EmpleadoModel)
        .options(
            joinedload(EmpleadoModel.tipo_empleado),
            joinedload(EmpleadoModel.area),
            joinedload(EmpleadoModel.contrato)
        )
    ).scalars().all()

    if not empleados:
        raise HTTPException(status_code=404, detail="No hay empleados registrados")

    # ✅ Convertimos a Pydantic incluyendo claves foráneas
    return [
        EmpleadoResponse(
            cod_empleado=empleado.cod_empleado,
            cod_persona=empleado.cod_persona,
            cod_tipo_empleado=empleado.cod_tipo_empleado,  # ✅ Agregamos el código
            cod_area=empleado.cod_area,  # ✅ Agregamos el código
            cod_tipo_contrato=empleado.cod_tipo_contrato,  # ✅ Agregamos el código
            nombre_tipo_empleado=empleado.tipo_empleado.nombre_tipo_empleado if empleado.tipo_empleado else None,
            nombre_area=empleado.area.nombre_area if empleado.area else None,
            tipo_contrato=empleado.contrato.tipo_contrato if empleado.contrato else None,
            fecha_salida=empleado.fecha_salida,
            motivo_salida=empleado.motivo_salida,
            fecha_contratacion=empleado.fecha_contratacion,
            salario=empleado.salario,
            estado_empleado=empleado.estado_empleado,
        )
        for empleado in empleados
    ]

# ✅ Endpoint para obtener un empleado por ID
@router.get("/empleados/{cod_empleado}", response_model=EmpleadoResponse)
def obtener_empleado_por_id_endpoint(cod_empleado: int, db: Session = Depends(get_sync_db)):
    empleado = db.execute(
        select(EmpleadoModel)
        .options(
            joinedload(EmpleadoModel.tipo_empleado),
            joinedload(EmpleadoModel.area),
            joinedload(EmpleadoModel.contrato)
        )
        .filter(EmpleadoModel.cod_empleado == cod_empleado)
    ).scalars().first()

    if not empleado:
        raise HTTPException(status_code=404, detail="Empleado no encontrado")

    # ✅ Convertimos la relación en un formato adecuado para la API
    return EmpleadoResponse(
        cod_empleado=empleado.cod_empleado,
        cod_persona=empleado.cod_persona,
        cod_tipo_empleado=empleado.cod_tipo_empleado,
        cod_area=empleado.cod_area,
        cod_tipo_contrato=empleado.cod_tipo_contrato,
        nombre_tipo_empleado=empleado.tipo_empleado.nombre_tipo_empleado if empleado.tipo_empleado else None,
        nombre_area=empleado.area.nombre_area if empleado.area else None,
        tipo_contrato=empleado.contrato.tipo_contrato if empleado.contrato else None,
        fecha_salida=empleado.fecha_salida,
        motivo_salida=empleado.motivo_salida,
        fecha_contratacion=empleado.fecha_contratacion,
        salario=empleado.salario,
        estado_empleado=empleado.estado_empleado,
    )

@router.post("/tipo_empleado/")
async def crear_tipo_empleado(nombre_tipo_empleado: NombreTipoEmpleadoCreate, db: AsyncSession = Depends(get_async_db)):
    try:
        await insertar_tipo_empleado(db, nombre_tipo_empleado)
        return {"message": "Tipo empleado insertado correctamente"}
    except Exception as e:
        error_message = str(e.orig) if hasattr(e, 'orig') else str(e)
        raise HTTPException(status_code=400, detail=error_message)

@router.get("/tipo_empleado/", response_model=List[NombreTipoEmpleado])
async def get_tipos_empleado(db: AsyncSession = Depends(get_async_db)):
    """
    Obtiene todos los registros de tipo_empleado.
    """
    try:
        tipos = await obtener_tipos_empleado(db)
        return tipos  # Si está vacío, retorna simplemente []
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/tipo_empleado/{cod_tipo_empleado}")
async def borrar_tipo_empleado(cod_tipo_empleado: int, db: AsyncSession = Depends(get_async_db)):
    try:
        db_nombre_tipo_empleado = await eliminar_tipo_empleado(db, cod_tipo_empleado)
        if db_nombre_tipo_empleado is None:
            raise HTTPException(status_code=404, detail="Tipo empleado no encontrado")
        return {"message": "Tipo empleado eliminado exitosamente"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/areas/")
async def crear_area(nombre_area: AreasCreate, db: AsyncSession = Depends(get_async_db)):
    try:
        await insertar_area(db, nombre_area)
        return {"message": "Área insertada correctamente"}
    except Exception as e:
        error_message = str(e.orig) if hasattr(e, 'orig') else str(e)
        raise HTTPException(status_code=400, detail=error_message)

@router.get("/areas/", response_model=List[AreasSchema])
async def get_areas(db: AsyncSession = Depends(get_async_db)):
    try:
        lista_areas = await obtener_areas(db)
        if not lista_areas:
            # Manejo de "no hay áreas"
            return []
        return lista_areas  # Retornamos la lista tal cual, FastAPI hará el parseo a AreasSchema
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/areas/{cod_area}")
async def borrar_area(cod_area: int, db: AsyncSession = Depends(get_async_db)):
    try:
        db_areas = await eliminar_area(db, cod_area)
        if db_areas is None:
            raise HTTPException(status_code=404, detail="Área no encontrada")
        return {"message": "Área eliminada exitosamente"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/tipo_contrato/")
async def crear_tipo_contrato(tipo_contrato: TipoContratoCreate, db: AsyncSession = Depends(get_async_db)):
    try:
        await insertar_tipo_contrato(db, tipo_contrato)
        return {"message": "Tipo de contrato insertado correctamente"}
    except Exception as e:
        error_message = str(e.orig) if hasattr(e, 'orig') else str(e)
        raise HTTPException(status_code=400, detail=error_message)

@router.get("/tipo_contrato/", response_model=List[TipoContrato])
async def get_tipos_contrato(db: AsyncSession = Depends(get_async_db)):
    """
    Devuelve todos los tipos de contrato registrados en la base de datos.
    """
    try:
        lista_contratos = await obtener_tipos_contrato(db)
        return lista_contratos
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/tipo_contrato/{cod_tipo_contrato}")
async def borrar_tipo_contrato(cod_tipo_contrato: int, db: AsyncSession = Depends(get_async_db)):
    try:
        db_tipo_contrato = await eliminar_tipo_contrato(db, cod_tipo_contrato)
        if db_tipo_contrato is None:
            raise HTTPException(status_code=404, detail="Tipo de contrato no encontrado")
        return {"message": "Tipo de contrato eliminado exitosamente"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

