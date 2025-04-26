from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_async_db, get_sync_db 
from sqlalchemy.sql import select, text
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.mandados_paquetes.mandados import MandadoCreate, MandadoUpdate, MandadoResponse
from app.models.mandados_paquetes.mandados import Mandado
from app.crud.mandados_paquetes.Mandados import (
    insertar_mandado_crud_async,
    actualizar_mandado_crud_async,
    eliminar_mandado_crud_async,
    obtener_mandados_crud_async
)
from typing import List
import logging

logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)

router = APIRouter()

@router.post("/mandados", response_model=dict)
async def crear_mandado(mandado: MandadoCreate, db: AsyncSession = Depends(get_async_db)):
    try:
        return await insertar_mandado_crud_async(db, mandado)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/mandados", response_model=dict)
async def modificar_mandado(mandado: MandadoUpdate, db: AsyncSession = Depends(get_async_db)):
    try:
        return await actualizar_mandado_crud_async(db, mandado)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/mandados{cod_mandado}", response_model=dict)
async def eliminar_mandado(cod_mandado: int, db: AsyncSession = Depends(get_async_db)):
    try:
        return await eliminar_mandado_crud_async(db, cod_mandado)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/mandados/", response_model=List[MandadoResponse])
async def listar_mandados(skip: int = 0, limit: int = 10, db: AsyncSession = Depends(get_async_db)):
    return await obtener_mandados_crud_async(db, skip=skip, limit=limit)

