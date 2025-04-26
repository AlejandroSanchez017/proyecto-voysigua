from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Literal
from app.database import get_async_db, get_sync_db
from app.crud.Personas.telefonos import (insertar_tipo_telefono, modificar_tipo_telefono, obtener_tipo_telefono_por_id, 
                                         eliminar_tipo_telefono, obtener_tipos_telefono, insertar_telefono,actualizar_telefono_crud,
                                         eliminar_telefono_crud, obtener_telefonos, obtener_telefono_por_id, obtener_telefonos_por_estado,
                                         obtener_telefonos_por_persona)
from app.schemas.Personas.telefonos import (TipoTelefonoCreate, TipoTelefonoUpdate, TipoTelefonoResponse, TelefonoCreate, TelefonoUpdate,
                                            TelefonoResponse)
from app.utils.utils import extraer_campo_foreign_key, extraer_campo_null
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

@router.post("/tipo_telefono/", response_model=dict)
async def crear_tipo_telefono(
    tipo: TipoTelefonoCreate,
    db: AsyncSession = Depends(get_async_db)
):
    try:
        result = await insertar_tipo_telefono(db, tipo)
        return result
    except Exception as e:
        logger.error(f"Error al crear tipo de teléfono: {e}")
        raise HTTPException(status_code=400, detail="No se pudo insertar el tipo de teléfono.")
    
@router.put("/tipo_telefono/{cod_tipo_telefono}", response_model=dict)
async def actualizar_tipo_telefono(
    cod_tipo_telefono: int,
    tipo: TipoTelefonoUpdate,
    db: AsyncSession = Depends(get_async_db)
):
    try:
        return await modificar_tipo_telefono(db, cod_tipo_telefono, tipo)

    except HTTPException as e:
        raise e  # Ya gestionado en el CRUD

    except Exception as e:
        logger.error(f"Error al actualizar tipo de teléfono: {e}")
        raise HTTPException(status_code=400, detail="No se pudo modificar el tipo de teléfono.")
    
@router.delete("/tipo_telefono/{cod_tipo_telefono}", response_model=dict)
async def eliminar_tipo_telefono_api(
    cod_tipo_telefono: int,
    db: AsyncSession = Depends(get_async_db)
):
    try:
        return await eliminar_tipo_telefono(db, cod_tipo_telefono)
    except HTTPException as e:
        raise e  # Ya gestionado en el CRUD
    except Exception as e:
        raise HTTPException(status_code=400, detail="No se pudo eliminar el tipo de teléfono.")
    
@router.get("/tipos_telefono", response_model=List[TipoTelefonoResponse])
def listar_tipos_telefono(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, gt=0),
    db: Session = Depends(get_sync_db)
):
    tipos = obtener_tipos_telefono(db, skip=skip, limit=limit)
    if not tipos:
        raise HTTPException(status_code=404, detail="No se encontraron tipos de teléfono")
    return tipos
    

@router.get("/tipo_telefono/{cod_tipo_telefono}", response_model=TipoTelefonoResponse)
async def obtener_tipo_telefono_api(
    cod_tipo_telefono: int,
    db: AsyncSession = Depends(get_async_db)
):
    try:
        return await obtener_tipo_telefono_por_id(db, cod_tipo_telefono)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error al consultar el tipo de teléfono.")
    
@router.post("/telefonos/", response_model=dict)
async def crear_telefono(telefono: TelefonoCreate, db: AsyncSession = Depends(get_async_db)):
    try:
        await insertar_telefono(db, telefono)
        return {"message": "Teléfono insertado exitosamente"}

    except IntegrityError as e:
        await db.rollback()
        error_msg = str(e.orig) if hasattr(e, "orig") else str(e)
        logger.error(f"Error de integridad al insertar teléfono: {error_msg}")

        # 🔍 Clave foránea inválida
        if "foreign key" in error_msg.lower() or "llave foránea" in error_msg.lower():
            campo = extraer_campo_foreign_key(error_msg)
            if campo == "cod_persona":
                raise HTTPException(
                    status_code=400,
                    detail="La persona indicada no existe. Verifica que 'cod_persona' sea válido."
                )
            if campo == "cod_tipo_telefono":
                raise HTTPException(
                    status_code=400,
                    detail="El tipo de teléfono indicado no existe. Verifica que 'cod_tipo_telefono' sea válido."
                )
            raise HTTPException(
                status_code=400,
                detail=f"El valor ingresado para '{campo}' no existe en la base de datos."
            )

        # ❗ Campo obligatorio omitido
        if "null value in column" in error_msg.lower():
            campo = extraer_campo_null(error_msg)
            raise HTTPException(
                status_code=400,
                detail=f"El campo '{campo}' es obligatorio y no puede estar vacío."
            )

        raise HTTPException(status_code=400, detail="Error de integridad en la base de datos.")

    except Exception as e:
        await db.rollback()
        logger.error(f"Error general al insertar teléfono: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
    
@router.put("/telefonos/{cod_telefono}", response_model=dict)
async def modificar_telefono(
    cod_telefono: int,
    telefono: TelefonoUpdate,
    db: AsyncSession = Depends(get_async_db)
):
    try:
        return await actualizar_telefono_crud(db, cod_telefono, telefono)

    except IntegrityError as e:
        error_msg = str(e.orig) if hasattr(e, "orig") else str(e)
        logger.error(f"Error de integridad al actualizar teléfono: {type(e.orig)} - {error_msg}")

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
        logger.error(f"Error general al actualizar teléfono: {error_str}")

        # 💡 Mensaje personalizado desde el procedimiento (si lo incluyeras)
        if "No se encontró el teléfono con ID" in error_str:
            raise HTTPException(
                status_code=404,
                detail=f"No se encontró el teléfono con ID {cod_telefono}"
            )

        raise HTTPException(status_code=400, detail=error_str)
    
@router.delete("/telefonos/{cod_telefono}", response_model=dict)
async def eliminar_telefono(
    cod_telefono: int,
    db: AsyncSession = Depends(get_async_db)
):
    try:
        return await eliminar_telefono_crud(db, cod_telefono)
    except HTTPException as e:
        raise e
    except Exception as e:
        logger.error(f"Error al eliminar teléfono: {str(e)}")
        raise HTTPException(status_code=500, detail="Error al eliminar el teléfono.")
    
@router.get("/telefonos/", response_model=List[TelefonoResponse])
def listar_telefonos(
    skip: int = Query(0, ge=0, description="Registros a omitir"),
    limit: int = Query(10, gt=0, description="Cantidad máxima de registros a devolver"),
    db: Session = Depends(get_sync_db)
):
    return obtener_telefonos(db, skip=skip, limit=limit)

@router.get("/telefonos/{cod_telefono}", response_model=TelefonoResponse)
def obtener_telefono(
    cod_telefono: int,
    db: Session = Depends(get_sync_db)
):
    return obtener_telefono_por_id(db, cod_telefono)

@router.get("/telefonos/estado/{estado}", response_model=List[TelefonoResponse])
def listar_telefonos_por_estado(
    estado: Literal["A", "I"],
    skip: int = Query(0, ge=0),
    limit: int = Query(10, gt=0),
    db: Session = Depends(get_sync_db)
):
    telefonos = obtener_telefonos_por_estado(db, estado, skip=skip, limit=limit)

    if not telefonos:
        raise HTTPException(
            status_code=404,
            detail=f"No se encontraron teléfonos con estado '{estado}'"
        )
    return telefonos

@router.get("/telefonos/persona/{cod_persona}", response_model=List[TelefonoResponse])
def listar_telefonos_por_persona(
    cod_persona: int,
    skip: int = Query(0, ge=0),
    limit: int = Query(10, gt=0),
    db: Session = Depends(get_sync_db)
):
    telefonos = obtener_telefonos_por_persona(db, cod_persona, skip=skip, limit=limit)

    if not telefonos:
        raise HTTPException(
            status_code=404,
            detail=f"No se encontraron teléfonos registrados para la persona con ID {cod_persona}"
        )
    return telefonos
    
