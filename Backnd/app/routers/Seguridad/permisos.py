from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
import logging
from app.database import get_async_db
from app.crud.Seguridad.permisos import (
    insertar_permiso,
    actualizar_permiso,
    eliminar_permiso,
    obtener_todos_los_permisos,
    obtener_permiso_por_id
)
from app.schemas.Seguridad.permisos import PermisoCreate, PermisoUpdate, PermisoResponse

router = APIRouter()
logger = logging.getLogger(__name__)

@router.post("/permisos/", response_model=dict)
async def create_permiso(permiso: PermisoCreate, db: AsyncSession = Depends(get_async_db)):
    try:
        result = await insertar_permiso(db, permiso)
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.put("/permisos/{permiso_id}", response_model=dict)
async def update_permiso(permiso_id: int, permiso: PermisoUpdate, db: AsyncSession = Depends(get_async_db)):
    try:
        result = await actualizar_permiso(db, permiso_id, permiso)
        return result
    except Exception as e:
        error_str = str(e)
        if "No se encontró el permiso con ID" in error_str:
            raise HTTPException(status_code=404, detail=f"No se encontró el permiso con ID {permiso_id}")
        else:
            raise HTTPException(status_code=400, detail=error_str)

@router.delete("/permisos/{permiso_id}", response_model=dict)
async def delete_permiso(permiso_id: int, db: AsyncSession = Depends(get_async_db)):
    try:
        result = await eliminar_permiso(db, permiso_id)
        return result
    except Exception as e:
        error_str = str(e)
        if "No se encontró el permiso con ID" in error_str:
            raise HTTPException(status_code=404, detail=f"No se encontró el permiso con ID {permiso_id}")
        else:
            raise HTTPException(status_code=400, detail=error_str)

@router.get("/permisos/", response_model=List[PermisoResponse])
async def get_permisos(db: AsyncSession = Depends(get_async_db)):
    try:
        permisos = await obtener_todos_los_permisos(db)
        return permisos
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/permisos/{permiso_id}", response_model=PermisoResponse)
async def get_permiso(permiso_id: int, db: AsyncSession = Depends(get_async_db)):
    try:
        permiso = await obtener_permiso_por_id(db, permiso_id)
        if permiso is None:
            raise HTTPException(status_code=404, detail=f"Permiso con ID {permiso_id} no encontrado")
        return permiso
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
