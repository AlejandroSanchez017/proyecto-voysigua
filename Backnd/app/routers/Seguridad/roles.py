from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session
from sqlalchemy.sql import select
from app.database import get_async_db, get_sync_db
from app.crud.Seguridad.roles import insertar_rol, actualizar_rol, eliminar_rol, buscar_rol_por_id
from app.schemas.Seguridad.roles import RoleCreate, RoleResponse, RoleUpdate
from app.models.Seguridad.roles import Role as RoleModel
from typing import List
import logging

logger = logging.getLogger(__name__)
router = APIRouter()

@router.post("/roles/")
async def crear_rol(
    role: RoleCreate,
    db: AsyncSession = Depends(get_async_db)
):
    """
    Crea un rol usando el stored procedure 'insertar_rol'
    y dispara el trigger de auditoría.
    """
    try:
        result = await insertar_rol(db, role)
        return result
    except Exception as e:
        logger.error(f"Error al crear rol: {e}")
        raise HTTPException(status_code=400, detail=str(e))
    
@router.get("/roles", response_model=List[RoleResponse])
def obtener_todas_los_roles(skip: int = 0, limit: int = 10, db: Session = Depends(get_sync_db)):  
    result = db.execute(select(RoleModel).offset(skip).limit(limit)) 
    return result.scalars().all()

@router.put("/roles/{role_id}")
async def update_rol(role_id: int, new_data: RoleUpdate, db: AsyncSession = Depends(get_async_db)):
    """
    Actualiza un rol mediante el stored procedure 'actualizar_rol'.
    """
    try:
        result = await actualizar_rol(db, role_id, new_data)
        return result
    except Exception as e:
        error_str = str(e)
        # Filtra el mensaje para no mostrar la traza completa
        if "No se encontró el rol con ID" in error_str:
            raise HTTPException(status_code=404, detail=f"No se encontró el rol con ID {role_id}")
        else:
            # Otros errores
            raise HTTPException(status_code=400, detail=error_str)
    
@router.delete("/roles/{role_id}")
async def delete_rol(role_id: int, db: AsyncSession = Depends(get_async_db)):
    try:
        result = await eliminar_rol(db, role_id)
        return result
    except Exception as e:
        error_str = str(e)
        # Si el procedure lanza "No se encontró el rol con ID X", 
        # detectamos esa subcadena en el mensaje
        if "No se encontró el rol con ID" in error_str:
            # Mostramos SOLO el texto limpio
            raise HTTPException(status_code=404, detail=f"No se encontró el rol con ID {role_id}")
        else:
            # Otros errores
            raise HTTPException(status_code=400, detail=error_str)
    
@router.get("/roles/{role_id}", response_model=RoleResponse)
async def get_rol_por_id(
    role_id: int,
    db: AsyncSession = Depends(get_async_db)
):
    """
    Llama al procedure 'buscar_rol_por_id(_id)' y luego
    hace SELECT para devolver la info del rol (id, name, guard, status).
    """
    try:
        rol_data = await buscar_rol_por_id(db, role_id)
        if rol_data is None:
            raise HTTPException(status_code=404, detail="Rol no encontrado")
        return rol_data
    except Exception as e:
        logger.error(f"Error al buscar rol por ID {role_id}: {e}")
        raise HTTPException(status_code=400, detail=str(e))