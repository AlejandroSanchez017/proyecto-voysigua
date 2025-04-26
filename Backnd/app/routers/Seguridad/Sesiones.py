from fastapi import APIRouter, Depends, HTTPException, Path
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_async_db
from app.schemas.Seguridad.Sesiones import SesionCreate, SesionResponse, SesionUsuarioResponse, SesionInactivaResponse
from app.crud.Seguridad.Sesiones import insertar_sesion, eliminar_sesion, consultar_sesion_por_id, eliminar_sesiones_antiguas, consultar_sesiones_por_usuario, cerrar_sesiones_por_usuario, consultar_sesiones_inactivas, eliminar_sesiones_inactivas
import logging
import re

router = APIRouter()
logger = logging.getLogger(__name__)

@router.post("/sesiones/", response_model=dict)
async def create_sesion(sesion: SesionCreate, db: AsyncSession = Depends(get_async_db)):
    try:
        result = await insertar_sesion(db, sesion)
        return result
    except Exception as e:
        logger.error(f"Error en create_sesion: {e}")
        raise HTTPException(status_code=400, detail="Error al insertar sesión.")


@router.delete("/sesiones/{id}", response_model=dict)
async def delete_sesion(id: str, db: AsyncSession = Depends(get_async_db)):
    try:
        result = await eliminar_sesion(db, id)
        return result
    except Exception as e:
        logger.error(f"Error en delete_sesion: {e}")
        raise HTTPException(status_code=400, detail="Error al eliminar sesión.")



@router.get("/sesiones/{id}", response_model=SesionResponse)
async def get_sesion_by_id(id: str, db: AsyncSession = Depends(get_async_db)):
    try:
        result = await consultar_sesion_por_id(db, id)
        return result
    except ValueError as ve:
        raise HTTPException(status_code=404, detail=str(ve))
    except Exception as e:
        logger.error(f"Error en get_sesion_by_id: {e}")
        raise HTTPException(status_code=400, detail="Error al consultar sesión.")

@router.delete("/sesiones/inactivas/{dias}", response_model=dict)
async def delete_sesiones_inactivas(dias: int, db: AsyncSession = Depends(get_async_db)):
    try:
        result = await eliminar_sesiones_antiguas(db, dias)
        return result
    except Exception as e:
        logger.error(f"Error en delete_sesiones_inactivas: {e}")
        raise HTTPException(status_code=400, detail="Error al eliminar sesiones inactivas.")
    
@router.get("/sesiones/usuario/{user_id}", response_model=list[SesionUsuarioResponse])
async def get_sesiones_por_usuario(user_id: int, db: AsyncSession = Depends(get_async_db)):
    try:
        result = await consultar_sesiones_por_usuario(db, user_id)
        return result
    except ValueError as ve:
        raise HTTPException(status_code=404, detail=str(ve))
    except Exception as e:
        logger.error(f"Error en get_sesiones_por_usuario: {e}")
        raise HTTPException(status_code=400, detail="Error al consultar sesiones del usuario.")
    
@router.delete("/sesiones/usuario/{user_id}", response_model=dict)
async def delete_sesiones_usuario(user_id: int, db: AsyncSession = Depends(get_async_db)):
    try:
        result = await cerrar_sesiones_por_usuario(db, user_id)
        return result
    except Exception as e:
        logger.error(f"Error en delete_sesiones_usuario: {e}")
        raise HTTPException(status_code=400, detail="Error al cerrar sesiones del usuario.")    
    

@router.get("/sesiones/inactivas/{intervalo}", response_model=list[SesionInactivaResponse])
async def get_sesiones_inactivas(
    intervalo: str = Path(..., description="Ej: '2 days', '3 hours'"),
    db: AsyncSession = Depends(get_async_db)
):
    if not re.match(r"^\d+\s+(day|days|hour|hours|minute|minutes)$", intervalo):
        raise HTTPException(status_code=400, detail="Intervalo inválido. Usa formatos como '2 days', '3 hours', '15 minutes'.")

    try:
        return await consultar_sesiones_inactivas(db, intervalo)
    except ValueError as ve:
        raise HTTPException(status_code=404, detail=str(ve))
    except Exception:
        raise HTTPException(status_code=400, detail="Error al consultar sesiones inactivas.")
    



@router.delete("/sesiones/inactivas/{intervalo}", response_model=dict)
async def delete_sesiones_inactivas_por_intervalo(
    intervalo: str = Path(..., description="Ej: '3 days', '4 hours', '15 minutes'"),
    db: AsyncSession = Depends(get_async_db)
):
    if not re.match(r"^\d+\s+(day|days|hour|hours|minute|minutes)$", intervalo):
        raise HTTPException(
            status_code=400,
            detail="Intervalo inválido. Usa formatos como '2 days', '4 hours', '30 minutes'."
        )

    try:
        result = await eliminar_sesiones_inactivas(db, intervalo)
        return result
    except Exception:
        raise HTTPException(status_code=400, detail="Error al eliminar sesiones inactivas.")