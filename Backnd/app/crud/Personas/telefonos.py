from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException
from sqlalchemy.orm import Session
from typing import List
from sqlalchemy import text
from sqlalchemy.future import select
from app.schemas.Personas.telefonos import TipoTelefonoCreate, TipoTelefonoUpdate, TelefonoCreate, TelefonoUpdate
from app.models.Personas.telefonos import TipoTelefono, Telefono
import logging

logger = logging.getLogger(__name__)

async def insertar_tipo_telefono(db: AsyncSession, tipo: TipoTelefonoCreate):
    query = text("CALL insertar_tipo_telefono(:nombre_tipo_telefono)")

    try:
        async with db.begin():
            await db.execute(query, {"nombre_tipo_telefono": tipo.nombre_tipo_telefono})
        return {"message": f"Tipo de teléfono '{tipo.nombre_tipo_telefono}' insertado exitosamente"}
    except Exception as e:
        logger.error(f"Error al insertar tipo de teléfono: {e}")
        raise

async def modificar_tipo_telefono(
    db: AsyncSession,
    cod_tipo_telefono: int,
    tipo: TipoTelefonoUpdate
):
    # 1️⃣ Verificar existencia
    result = await db.execute(
        select(TipoTelefono)
        .where(TipoTelefono.cod_tipo_telefono == cod_tipo_telefono)
    )
    existente = result.scalars().first()
    if not existente:
        raise HTTPException(
            status_code=404,
            detail=f"No se encontró el tipo de teléfono con ID {cod_tipo_telefono}"
        )

    # 2️⃣ Si existe, llamamos al procedimiento
    query = text(
        "CALL modificar_tipo_telefono(:cod_tipo_telefono, :nombre_tipo_telefono)"
    )
    try:
        await db.execute(query, {
            "cod_tipo_telefono": cod_tipo_telefono,
            "nombre_tipo_telefono": tipo.nombre_tipo_telefono
        })
        await db.commit()
        return {"message": f"Tipo de teléfono con ID {cod_tipo_telefono} modificado exitosamente"}
    except Exception as e:
        await db.rollback()
        # Aquí podrías capturar errores puntuales de tu SP si hacen RAISE
        raise HTTPException(
            status_code=500,
            detail="Error interno al modificar el tipo de teléfono."
        )

def obtener_tipos_telefono(db: Session, skip: int = 0, limit: int = 10):
    return db.query(TipoTelefono).offset(skip).limit(limit).all()

async def eliminar_tipo_telefono(db: AsyncSession, cod_tipo_telefono: int):
    # Validar si existe antes de ejecutar el procedimiento
    result = await db.execute(select(TipoTelefono).where(TipoTelefono.cod_tipo_telefono == cod_tipo_telefono))
    tipo = result.scalar_one_or_none()

    if not tipo:
        raise HTTPException(status_code=404, detail=f"No se encontró el tipo de teléfono con ID {cod_tipo_telefono}")

    query = text("CALL eliminar_tipo_telefono(:_cod_tipo_telefono)")
    
    try:
        await db.execute(query, {"_cod_tipo_telefono": cod_tipo_telefono})
        await db.commit()
        return {"message": f"Tipo de teléfono con ID {cod_tipo_telefono} eliminado exitosamente"}
    
    except Exception as e:
        await db.rollback()
        error_str = str(e)
        if "está en uso" in error_str:
            raise HTTPException(status_code=400, detail="Este tipo de teléfono está en uso y no se puede eliminar.")
        raise HTTPException(status_code=500, detail="Error interno al eliminar el tipo de teléfono.")
    
async def obtener_tipo_telefono_por_id(db: AsyncSession, cod_tipo_telefono: int):
    result = await db.execute(
        select(TipoTelefono).where(TipoTelefono.cod_tipo_telefono == cod_tipo_telefono)
    )
    tipo = result.scalar_one_or_none()

    if tipo is None:
        raise HTTPException(status_code=404, detail=f"No se encontró el tipo de teléfono con ID {cod_tipo_telefono}")
    return tipo

async def insertar_telefono(db: AsyncSession, telefono: TelefonoCreate):
    query = text("""
        CALL insertar_telefono(
            :_cod_persona,
            :_telefono_principal,
            :_exten,
            :_codigo_area,
            :_cod_tipo_telefono,
            :_estado
        )
    """)
    try:
        await db.execute(query, {
            "_cod_persona": telefono.cod_persona,
            "_telefono_principal": telefono.telefono_principal,
            "_exten": telefono.exten,
            "_codigo_area": telefono.codigo_area,
            "_cod_tipo_telefono": telefono.cod_tipo_telefono,
            "_estado": telefono.estado,
        })
        await db.commit()
    except Exception as e:
        await db.rollback()
        raise e
    

async def actualizar_telefono_crud(db: AsyncSession, cod_telefono: int, telefono: TelefonoUpdate):
    # Validar existencia antes del procedimiento
    result = await db.execute(select(Telefono).where(Telefono.cod_telefono == cod_telefono))
    existe = result.scalar_one_or_none()

    if not existe:
        raise HTTPException(status_code=404, detail=f"No se encontró el teléfono con ID {cod_telefono}")

    query = text("""
        CALL actualizar_telefono(
            :_cod_telefono,
            :_telefono_principal,
            :_exten,
            :_codigo_area,
            :_cod_tipo_telefono,
            :_estado
        )
    """)

    try:
        await db.execute(query, {
            "_cod_telefono": cod_telefono,
            "_telefono_principal": telefono.telefono_principal,
            "_exten": telefono.exten,
            "_codigo_area": telefono.codigo_area,
            "_cod_tipo_telefono": telefono.cod_tipo_telefono,
            "_estado": telefono.estado,
        })
        await db.commit()
        return {"message": f"Teléfono con ID {cod_telefono} actualizado correctamente"}
    except Exception as e:
        await db.rollback()
        raise

async def eliminar_telefono_crud(db: AsyncSession, cod_telefono: int):
    # Validar si el teléfono existe
    result = await db.execute(select(Telefono).where(Telefono.cod_telefono == cod_telefono))
    telefono = result.scalar_one_or_none()

    if not telefono:
        raise HTTPException(
            status_code=404,
            detail=f"No se encontró el teléfono con ID {cod_telefono}"
        )

    query = text("CALL eliminar_telefono(:_cod_telefono)")

    try:
        await db.execute(query, {"_cod_telefono": cod_telefono})
        await db.commit()
        return {"message": f"Teléfono con ID {cod_telefono} eliminado exitosamente"}
    except Exception as e:
        await db.rollback()
        raise

def obtener_telefonos(db: Session,skip: int = 0,limit: int = 10) -> List[Telefono]:
    return (db.query(Telefono).offset(skip).limit(limit).all())

def obtener_telefono_por_id(db: Session,cod_telefono: int) -> Telefono:
    telefono = (db.query(Telefono).filter(Telefono.cod_telefono == cod_telefono).first())
    if not telefono:
        raise HTTPException(status_code=404,detail=f"No se encontró el teléfono con ID {cod_telefono}")
    return telefono

def obtener_telefonos_por_estado(db: Session,estado: str,skip: int = 0,limit: int = 10) -> List[Telefono]:
    return (db.query(Telefono).filter(Telefono.estado == estado).offset(skip).limit(limit).all())

def obtener_telefonos_por_persona(db: Session,cod_persona: int,skip: int = 0,limit: int = 10) -> List[Telefono]:
    return (db.query(Telefono).filter(Telefono.cod_persona == cod_persona).offset(skip).limit(limit).all()
    )