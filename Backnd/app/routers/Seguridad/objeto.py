from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_async_db
from app.schemas.Seguridad.objeto import ObjetoCreate, ObjetoUpdate, ObjetoResponse
from app.crud.Seguridad.objeto import insertar_objeto, actualizar_objeto, eliminar_objeto, consultar_objeto_por_id, consultar_todos_objetos
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

@router.post("/objetos/", response_model=dict)
async def create_objeto(objeto: ObjetoCreate, db: AsyncSession = Depends(get_async_db)):
    try:
        result = await insertar_objeto(db, objeto)
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
    
@router.put("/objetos/{id}", response_model=dict)
async def update_objeto(id: int, objeto: ObjetoUpdate, db: AsyncSession = Depends(get_async_db)):
    try:
        result = await actualizar_objeto(db, id, objeto)
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/objetos/{id}", response_model=dict)
async def delete_objeto(id: int, db: AsyncSession = Depends(get_async_db)):

    try:
        result = await eliminar_objeto(db, id)
        return result
    except Exception as e:
        logger.error(f"Error en delete_objeto: {e}")
        raise HTTPException(status_code=400, detail=str(e))
    
@router.get("/objetos/{id}", response_model=ObjetoResponse)
async def get_objeto_por_id(id: int, db: AsyncSession = Depends(get_async_db)):
    try:
        result = await consultar_objeto_por_id(db, id)
        return result
    except ValueError as ve:
        raise HTTPException(status_code=404, detail=str(ve))
    except Exception as e:
        logger.error(f"Error en get_objeto_por_id: {e}")
        raise HTTPException(status_code=400, detail="Error al consultar objeto.")
    
@router.get("/objetos/", response_model=list[ObjetoResponse])
async def get_all_objetos(db: AsyncSession = Depends(get_async_db)):
    try:
        result = await consultar_todos_objetos(db)
        return result
    except Exception as e:
        logger.error(f"Error en get_all_objetos: {e}")
        raise HTTPException(status_code=400, detail="Error al consultar objetos.") 
  