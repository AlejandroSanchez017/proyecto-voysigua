from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_async_db
from app.schemas.Seguridad.parametros import ParametroCreate, ParametroUpdate, ParametroResponse
from app.crud.Seguridad.parametros import insertar_parametro, actualizar_parametro, inactivar_parametro, consultar_parametro_por_id, consultar_todos_parametros, consultar_parametros_por_estado, consultar_parametros_por_categoria
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

@router.post("/parametros/", response_model=dict)
async def create_parametro(parametro: ParametroCreate, db: AsyncSession = Depends(get_async_db)):
    try:
        result = await insertar_parametro(db, parametro)
        return result
    except Exception as e:
        logger.error(f"Error en create_parametro: {e}")
        raise HTTPException(status_code=400, detail="Error al insertar parámetro.")

@router.put("/parametros/{id}", response_model=dict)
async def update_parametro(id: int, parametro: ParametroUpdate, db: AsyncSession = Depends(get_async_db)):
    try:
        result = await actualizar_parametro(db, id, parametro)
        return result
    except Exception as e:
        logger.error(f"Error en update_parametro: {e}")
        raise HTTPException(status_code=400, detail="Error al actualizar parámetro.")
    
 

@router.put("/parametros/inactivar/{id}", response_model=dict)
async def put_inactivar_parametro(id: int, db: AsyncSession = Depends(get_async_db)):
    try:
        result = await inactivar_parametro(db, id)
        return result
    except Exception as e:
        logger.error(f"Error en put_inactivar_parametro: {e}")
        raise HTTPException(status_code=400, detail="Error al inactivar parámetro.")
    
@router.get("/parametros/{id}", response_model=ParametroResponse)
async def get_parametro_por_id(id: int, db: AsyncSession = Depends(get_async_db)):
    try:
        result = await consultar_parametro_por_id(db, id)
        return result
    except ValueError as ve:
        raise HTTPException(status_code=404, detail=str(ve))
    except Exception as e:
        logger.error(f"Error en get_parametro_por_id: {e}")
        raise HTTPException(status_code=400, detail="Error al consultar el parámetro.")   


@router.get("/parametros/", response_model=list[ParametroResponse])
async def get_all_parametros(db: AsyncSession = Depends(get_async_db)):
    try:
        result = await consultar_todos_parametros(db)
        return result
    except Exception as e:
        logger.error(f"Error en get_all_parametros: {e}")
        raise HTTPException(status_code=400, detail="Error al consultar parámetros.")
    
@router.get("/parametros/estado/{estado}", response_model=list[ParametroResponse])
async def get_parametros_por_estado(estado: str, db: AsyncSession = Depends(get_async_db)):
    try:
        if estado not in ["activo", "inactivo"]:
            raise HTTPException(status_code=400, detail="Estado inválido. Debe ser 'activo' o 'inactivo'.")
        
        result = await consultar_parametros_por_estado(db, estado)
        return result
    except ValueError as ve:
        raise HTTPException(status_code=404, detail=str(ve))
    except Exception as e:
        logger.error(f"Error en get_parametros_por_estado: {e}")
        raise HTTPException(status_code=400, detail="Error al consultar parámetros por estado.")   

@router.get("/parametros/categoria/{categoria}", response_model=list[ParametroResponse])
async def get_parametros_por_categoria(categoria: str, db: AsyncSession = Depends(get_async_db)):
    try:
        result = await consultar_parametros_por_categoria(db, categoria)
        return result
    except ValueError as ve:
        raise HTTPException(status_code=404, detail=str(ve))
    except Exception as e:
        logger.error(f"Error en get_parametros_por_categoria: {e}")
        raise HTTPException(status_code=400, detail="Error al consultar parámetros por categoría.")
