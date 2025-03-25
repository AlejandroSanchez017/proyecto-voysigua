from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from sqlalchemy import text
from typing import List
from app.database import get_async_db
from app.schemas.Seguridad.model_to_rol import AsignarRolRequest
from app.crud.Seguridad.model_to_rol import asignar_rol_a_modelo_crud, revocar_rol_de_modelo_crud, consultar_roles_por_modelo_crud, consultar_modelos_por_rol_crud
from app.utils.utils import extraer_campo_foreign_key
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

@router.post("/role-to-model", response_model=dict)
async def asignar_rol(datos: AsignarRolRequest, db: AsyncSession = Depends(get_async_db)):
    try:
        await asignar_rol_a_modelo_crud(db, datos)
        return {"message": "Rol asignado correctamente al modelo"}

    except IntegrityError as e:
        error_msg = str(e.orig) if hasattr(e, "orig") else str(e)
        logger.error(f"Error de integridad al asignar rol: {error_msg}")

        if "foreign key" in error_msg.lower() or "llave foránea" in error_msg.lower():
            campo = extraer_campo_foreign_key(error_msg)
            raise HTTPException(
                status_code=400,
                detail=f"El valor ingresado para '{campo}' no existe en la base de datos."
            )

        raise HTTPException(status_code=400, detail="Error de integridad en la base de datos.")

    except Exception as e:
        logger.error(f"Error general al asignar rol: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))  
    
    
@router.delete("/role-to-model/revoke", response_model=dict)
async def revocar_rol(
    datos: AsignarRolRequest,
    db: AsyncSession = Depends(get_async_db)
):
    try:
        result = await revocar_rol_de_modelo_crud(db, datos)
        return result

    except IntegrityError as e:
        error_msg = str(e.orig) if hasattr(e, "orig") else str(e)
        logger.error(f"Error de integridad al revocar rol: {error_msg}")
        raise HTTPException(status_code=400, detail="Error de integridad en la base de datos.")

    except Exception as e:
        logger.error(f"Error general al revocar rol: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
    
@router.get("/model-roles", response_model=List[dict])
async def obtener_modelos_con_roles(db: AsyncSession = Depends(get_async_db)):
    query = text("SELECT * FROM model_has_roles")
    result = await db.execute(query)
    rows = result.fetchall()
    return [dict(row._mapping) for row in rows]
    
@router.get("/roles-por-modelo/{tipo_modelo}/{id_modelo}", response_model=list[dict])
async def obtener_roles_de_modelo(
    tipo_modelo: str,
    id_modelo: int,
    db: AsyncSession = Depends(get_async_db)
):
    return await consultar_roles_por_modelo_crud(db, tipo_modelo, id_modelo)

@router.get("/roles/{role_id}/modelos", response_model=list[dict])
async def obtener_modelos_por_rol(
    role_id: int,
    db: AsyncSession = Depends(get_async_db)
):
    return await consultar_modelos_por_rol_crud(db, role_id)