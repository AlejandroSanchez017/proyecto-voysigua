from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.exc import IntegrityError
from typing import List, Literal
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession
from app.utils.utils import extraer_campo_foreign_key, extraer_campo_null
from app.schemas.Personas.direcciones import (DepartamentoCreate, DepartamentoUpdate, DepartamentoResponse, CiudadCreate, CiudadUpdate,
                                              CiudadResponse, TipoDireccionCreate, TipoDireccionUpdate, TipoDireccionResponse, 
                                              DireccionCreate, DireccionUpdate, DireccionResponse)
from app.crud.Personas.direcciones import (insertar_departamento, modificar_departamento, eliminar_departamento, obtener_departamentos, 
                                           obtener_departamento_por_id, insertar_ciudad, modificar_ciudad, eliminar_ciudad, 
                                           obtener_ciudades, obtener_ciudad_por_id, insertar_tipo_direccion, modificar_tipo_direccion,
                                           eliminar_tipo_direccion, obtener_tipos_direccion, obtener_tipo_direccion_por_id,
                                           insertar_direccion, actualizar_direccion_crud, eliminar_direccion_crud, obtener_direcciones,
                                           obtener_direccion_por_id, obtener_direcciones_por_estado, obtener_direcciones_por_persona)
from app.database import get_async_db, get_sync_db
import logging

logger = logging.getLogger(__name__)
router = APIRouter()

@router.post("/departamento/", response_model=dict)
async def crear_departamento(
    departamento: DepartamentoCreate,
    db: AsyncSession = Depends(get_async_db)
):
    try:
        return await insertar_departamento(db, departamento)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error al insertar el departamento.")
    
@router.put("/departamento/{cod_departamento}", response_model=dict)
async def actualizar_departamento(
    cod_departamento: int,
    departamento: DepartamentoUpdate,
    db: AsyncSession = Depends(get_async_db)
):
    try:
        return await modificar_departamento(db, cod_departamento, departamento)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error al modificar el departamento.")
    
@router.delete("/departamento/{cod_departamento}", response_model=dict)
async def eliminar_departamento_api(
    cod_departamento: int,
    db: AsyncSession = Depends(get_async_db)
):
    try:
        return await eliminar_departamento(db, cod_departamento)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail="No se pudo eliminar el departamento.")
    
@router.get("/departamentos", response_model=List[DepartamentoResponse])
def listar_departamentos(
    skip: int = Query(0, ge=0, description="Cantidad de registros a omitir"),
    limit: int = Query(10, gt=0, description="Cantidad máxima de registros a devolver"),
    db: Session = Depends(get_sync_db)
):
    return obtener_departamentos(db, skip=skip, limit=limit)

@router.get("/departamento/{cod_departamento}", response_model=DepartamentoResponse)
def obtener_departamento(
    cod_departamento: int,
    db: Session = Depends(get_sync_db)
):
    return obtener_departamento_por_id(db, cod_departamento)

@router.post("/ciudad/", response_model=dict)
async def crear_ciudad(
    ciudad: CiudadCreate,
    db: AsyncSession = Depends(get_async_db)
):
    try:
        return await insertar_ciudad(db, ciudad)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error al insertar la ciudad.")
    
@router.put("/ciudad/{cod_ciudad}", response_model=dict)
async def actualizar_ciudad(
    cod_ciudad: int,
    ciudad: CiudadUpdate,
    db: AsyncSession = Depends(get_async_db)
):
    try:
        return await modificar_ciudad(db, cod_ciudad, ciudad)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error al modificar la ciudad.")
    
@router.delete("/ciudad/{cod_ciudad}", response_model=dict)
async def eliminar_ciudad_api(
    cod_ciudad: int,
    db: AsyncSession = Depends(get_async_db)
):
    try:
        return await eliminar_ciudad(db, cod_ciudad)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail="No se pudo eliminar la ciudad.")
    
@router.get("/ciudades", response_model=List[CiudadResponse])
def listar_ciudades(
    skip: int = Query(0, ge=0, description="Registros a omitir"),
    limit: int = Query(10, gt=0, description="Cantidad máxima de registros a devolver"),
    db: Session = Depends(get_sync_db)
):
    return obtener_ciudades(db, skip=skip, limit=limit)

@router.get("/ciudad/{cod_ciudad}", response_model=CiudadResponse)
def obtener_ciudad(
    cod_ciudad: int,
    db: Session = Depends(get_sync_db)
):
    return obtener_ciudad_por_id(db, cod_ciudad)

@router.post("/tipo_direccion/", response_model=dict)
async def crear_tipo_direccion(
    tipo: TipoDireccionCreate,
    db: AsyncSession = Depends(get_async_db)
):
    try:
        return await insertar_tipo_direccion(db, tipo)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error al insertar el tipo de dirección.")
    
@router.put("/tipo_direccion/{cod_tipo_direccion}", response_model=dict)
async def actualizar_tipo_direccion(
    cod_tipo_direccion: int,
    tipo: TipoDireccionUpdate,
    db: AsyncSession = Depends(get_async_db)
):
    try:
        return await modificar_tipo_direccion(db, cod_tipo_direccion, tipo)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error al modificar el tipo de dirección.")
    
@router.delete("/tipo_direccion/{cod_tipo_direccion}", response_model=dict)
async def eliminar_tipo_direccion_api(
    cod_tipo_direccion: int,
    db: AsyncSession = Depends(get_async_db)
):
    try:
        return await eliminar_tipo_direccion(db, cod_tipo_direccion)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail="No se pudo eliminar el tipo de dirección.")
    
@router.get("/tipo_direccion", response_model=List[TipoDireccionResponse])
def listar_tipos_direccion(
    skip: int = Query(0, ge=0, description="Registros a omitir"),
    limit: int = Query(10, gt=0, description="Cantidad máxima de registros a devolver"),
    db: Session = Depends(get_sync_db)
):
    return obtener_tipos_direccion(db, skip=skip, limit=limit)


@router.get("/tipo_direccion/{cod_tipo_direccion}", response_model=TipoDireccionResponse)
def obtener_tipo_direccion(
    cod_tipo_direccion: int,
    db: Session = Depends(get_sync_db)
):
    return obtener_tipo_direccion_por_id(db, cod_tipo_direccion)
    
@router.post("/direccion/", response_model=dict)
async def crear_direccion(
    direccion: DireccionCreate,
    cod_persona: int = Query(..., description="ID de la persona asociada"),
    db: AsyncSession = Depends(get_async_db),
):
    try:
        await insertar_direccion(db, direccion, cod_persona)  # ✅ PASAMOS cod_persona
        return {"message": "Dirección insertada exitosamente"}

    except IntegrityError as e:
        await db.rollback()
        error_msg = str(e.orig) if hasattr(e, "orig") else str(e)
        logger.error(f"Error de integridad al insertar dirección: {error_msg}")

        if "foreign key" in error_msg.lower() or "llave foránea" in error_msg.lower():
            campo = extraer_campo_foreign_key(error_msg)
            raise HTTPException(
                status_code=400,
                detail=f"El valor ingresado para '{campo}' no existe en la base de datos. Verifica que sea válido."
            )

        if "null value in column" in error_msg.lower():
            campo = extraer_campo_null(error_msg)
            raise HTTPException(
                status_code=400,
                detail=f"El campo '{campo}' es obligatorio y no puede estar vacío."
            )

        raise HTTPException(status_code=400, detail="Error de integridad en la base de datos.")

    except Exception as e:
        await db.rollback()
        logger.error(f"Error general al insertar dirección: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
    
@router.put("/direccion/{cod_direccion}", response_model=dict)
async def modificar_direccion(
    cod_direccion: int,
    direccion: DireccionUpdate,
    db: AsyncSession = Depends(get_async_db)
):
    try:
        return await actualizar_direccion_crud(db, cod_direccion, direccion)

    except IntegrityError as e:
        error_msg = str(e.orig) if hasattr(e, "orig") else str(e)
        logger.error(f"Error de integridad al actualizar dirección: {type(e.orig)} - {error_msg}")

        # 🔍 Clave foránea inválida
        if "foreign key" in error_msg.lower() or "llave foránea" in error_msg.lower():
            campo = extraer_campo_foreign_key(error_msg)
            raise HTTPException(
                status_code=400,
                detail=f"El valor ingresado para '{campo}' no existe en la base de datos. Verifica que sea válido."
            )

        # ⚠️ Campo obligatorio omitido
        if "null value in column" in error_msg.lower():
            campo = extraer_campo_null(error_msg)
            raise HTTPException(
                status_code=400,
                detail=f"El campo '{campo}' es obligatorio y no puede estar vacío."
            )

        raise HTTPException(status_code=400, detail="Error de integridad en la base de datos.")

    except Exception as e:
        error_str = str(e)
        logger.error(f"Error general al actualizar dirección: {error_str}")

        # 💡 Mensaje personalizado desde el procedimiento (si algún día lo agregas)
        if "No se encontró la dirección con ID" in error_str:
            raise HTTPException(
                status_code=404,
                detail=f"No se encontró la dirección con ID {cod_direccion}"
            )
        raise HTTPException(status_code=400, detail=error_str)
    
@router.delete("/direccion/{cod_direccion}", response_model=dict)
async def eliminar_direccion(
    cod_direccion: int,
    db: AsyncSession = Depends(get_async_db)
):
    try:
        return await eliminar_direccion_crud(db, cod_direccion)

    except HTTPException as e:
        raise e

    except Exception as e:
        logger.error(f"Error al eliminar dirección: {str(e)}")
        raise HTTPException(status_code=500, detail="Error al eliminar la dirección.")
    
@router.get("/direcciones/", response_model=List[DireccionResponse])
def listar_direcciones(
    skip: int = Query(0, ge=0, description="Registros a omitir"),
    limit: int = Query(10, gt=0, description="Cantidad máxima de registros a devolver"),
    db: Session = Depends(get_sync_db)
):
    direcciones = obtener_direcciones(db, skip=skip, limit=limit)

    if not direcciones:
        raise HTTPException(
            status_code=404,
            detail="No se encontraron direcciones registradas"
        )
    return direcciones

@router.get("/direccion/{cod_direccion}", response_model=DireccionResponse)
def obtener_direccion(
    cod_direccion: int,
    db: Session = Depends(get_sync_db)
):
    return obtener_direccion_por_id(db, cod_direccion)

@router.get("/direcciones/estado/{estado}", response_model=List[DireccionResponse])
def listar_direcciones_por_estado(
    estado: Literal["A", "I"],
    skip: int = Query(0, ge=0),
    limit: int = Query(10, gt=0),
    db: Session = Depends(get_sync_db)
):
    direcciones = obtener_direcciones_por_estado(db, estado, skip=skip, limit=limit)

    if not direcciones:
        raise HTTPException(
            status_code=404,
            detail=f"No se encontraron direcciones con estado '{estado}'"
        )
    return direcciones


@router.get("/direcciones/persona/{cod_persona}", response_model=List[DireccionResponse])
def listar_direcciones_por_persona(
    cod_persona: int,
    skip: int = Query(0, ge=0),
    limit: int = Query(10, gt=0),
    db: Session = Depends(get_sync_db)
):
    direcciones = obtener_direcciones_por_persona(db, cod_persona, skip=skip, limit=limit)

    if not direcciones:
        raise HTTPException(
            status_code=404,
            detail=f"No se encontraron direcciones registradas para la persona con ID {cod_persona}"
        )
    return direcciones
