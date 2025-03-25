from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from app.database import get_async_db
from sqlalchemy import text
from typing import List
from app.schemas.Seguridad.model_to_permission import AsignarPermisoRequest
from app.crud.Seguridad.model_to_permission import asignar_permiso_a_modelo_crud, revocar_permiso_de_modelo_crud, consultar_permisos_por_modelo_crud, consultar_modelos_por_permiso_crud
from app.utils.utils import extraer_campo_foreign_key
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

router = APIRouter()

@router.post("/permission-to-model", response_model=dict)
async def asignar_permiso(
    datos: AsignarPermisoRequest,
    db: AsyncSession = Depends(get_async_db)
):
    try:
        return await asignar_permiso_a_modelo_crud(db, datos)

    except IntegrityError as e:
        error_msg = str(e.orig) if hasattr(e, "orig") else str(e)
        logger.error(f"Error de integridad al asignar permiso: {error_msg}")

        if "foreign key" in error_msg.lower() or "llave foránea" in error_msg.lower():
            campo = extraer_campo_foreign_key(error_msg)
            raise HTTPException(
                status_code=400,
                detail=f"El valor ingresado para '{campo}' no existe en la base de datos."
            )

        raise HTTPException(status_code=400, detail="Error de integridad en la base de datos.")

    except Exception as e:
        logger.error(f"Error general al asignar permiso: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/permission-to-model/revoke", response_model=dict)
async def revocar_permiso(
    datos: AsignarPermisoRequest,
    db: AsyncSession = Depends(get_async_db)
):
    try:
        return await revocar_permiso_de_modelo_crud(db, datos)

    except IntegrityError as e:
        error_msg = str(e.orig) if hasattr(e, "orig") else str(e)
        logger.error(f"Error de integridad al revocar permiso: {error_msg}")

        if "foreign key" in error_msg.lower() or "llave foránea" in error_msg.lower():
            campo = extraer_campo_foreign_key(error_msg)
            raise HTTPException(
                status_code=400,
                detail=f"El valor ingresado para '{campo}' no existe en la base de datos."
            )

        raise HTTPException(status_code=400, detail="Error de integridad en la base de datos.")

    except Exception as e:
        logger.error(f"Error general al revocar permiso: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
    
@router.get("/model-permisos", response_model=List[dict])
async def obtener_modelos_con_permisos(db: AsyncSession = Depends(get_async_db)):
    query = text("SELECT * FROM model_has_permissions")
    result = await db.execute(query)
    rows = result.fetchall()
    return [dict(row._mapping) for row in rows]
    
@router.get("/permisos-por-modelo/{tipo_modelo}/{id_modelo}", response_model=list[dict])
async def obtener_permisos_de_modelo(
    tipo_modelo: str,
    id_modelo: int,
    db: AsyncSession = Depends(get_async_db)
):
    return await consultar_permisos_por_modelo_crud(db, tipo_modelo, id_modelo)

@router.get("/permisos/{permission_id}/modelos", response_model=list[dict])
async def obtener_modelos_por_permiso(
    permission_id: int,
    db: AsyncSession = Depends(get_async_db)
):
    return await consultar_modelos_por_permiso_crud(db, permission_id)