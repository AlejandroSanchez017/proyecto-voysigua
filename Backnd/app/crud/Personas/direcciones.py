from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text, select
from typing import List
from sqlalchemy.orm import Session
from app.schemas.Personas.direcciones import (DepartamentoCreate, DepartamentoUpdate, CiudadCreate, CiudadUpdate, TipoDireccionCreate, 
                                              TipoDireccionUpdate, DireccionCreate, DireccionUpdate)
from app.models.Personas.direcciones import Departamento, Ciudad, TipoDireccion, Direccion
from fastapi import HTTPException
import logging

logger = logging.getLogger(__name__)

async def insertar_departamento(db: AsyncSession, departamento: DepartamentoCreate):
    query = text("CALL insertar_departamento(:_nombre_departamento)")

    try:
        async with db.begin():
            await db.execute(query, {"_nombre_departamento": departamento.nombre_departamento})
        return {"message": f"Departamento '{departamento.nombre_departamento}' insertado exitosamente"}
    except Exception as e:
        logger.error(f"Error al insertar departamento: {e}")
        raise HTTPException(status_code=400, detail="No se pudo insertar el departamento.")
    
async def modificar_departamento(
    db: AsyncSession,
    cod_departamento: int,
    departamento: DepartamentoUpdate
):
    # Validar si existe
    result = await db.execute(
        select(Departamento).where(Departamento.cod_departamento == cod_departamento)
    )
    existente = result.scalar_one_or_none()

    if not existente:
        raise HTTPException(
            status_code=404,
            detail=f"No se encontró el departamento con ID {cod_departamento}"
        )

    query = text("CALL modificar_departamento(:_cod_departamento, :_nombre_departamento)")

    try:
        await db.execute(query, {
            "_cod_departamento": cod_departamento,
            "_nombre_departamento": departamento.nombre_departamento
        })
        await db.commit()
        return {"message": f"Departamento con ID {cod_departamento} modificado exitosamente"}
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=400, detail="No se pudo modificar el departamento.")
    
async def eliminar_departamento(db: AsyncSession, cod_departamento: int):
    # Validar si el departamento existe antes de llamar al procedimiento
    result = await db.execute(
        select(Departamento).where(Departamento.cod_departamento == cod_departamento)
    )
    existente = result.scalar_one_or_none()

    if not existente:
        raise HTTPException(status_code=404, detail=f"No se encontró el departamento con ID {cod_departamento}")

    query = text("CALL eliminar_departamento(:_cod_departamento)")

    try:
        await db.execute(query, {"_cod_departamento": cod_departamento})
        await db.commit()
        return {"message": f"Departamento con ID {cod_departamento} eliminado exitosamente"}
    except Exception as e:
        await db.rollback()
        error_str = str(e)

        if "está en uso por" in error_str.lower():
            raise HTTPException(
                status_code=400,
                detail="Este departamento está en uso por una o más ciudades y no se puede eliminar."
            )

        raise HTTPException(status_code=500, detail="Error interno al eliminar el departamento.")
    
def obtener_departamentos(
    db: Session,skip: int = 0,limit: int = 10) -> List[Departamento]:
    return (db.query(Departamento).offset(skip).limit(limit).all())

def obtener_departamento_por_id(
    db: Session,cod_departamento: int) -> Departamento:
    departamento = (db.query(Departamento).filter(Departamento.cod_departamento == cod_departamento).first())

    if not departamento:
        raise HTTPException(status_code=404,detail=f"No se encontró el departamento con ID {cod_departamento}")
    return departamento

async def insertar_ciudad(db: AsyncSession, ciudad: CiudadCreate):
    query = text("CALL insertar_ciudad(:_nombre_ciudad, :_cod_departamento)")

    try:
        async with db.begin():
            await db.execute(query, {
                "_nombre_ciudad": ciudad.nombre_ciudad,
                "_cod_departamento": ciudad.cod_departamento
            })
        return {"message": f"Ciudad '{ciudad.nombre_ciudad}' insertada exitosamente"}
    except Exception as e:
        logger.error(f"Error al insertar ciudad: {e}")
        raise HTTPException(status_code=400, detail="No se pudo insertar la ciudad.")
    
async def insertar_ciudad(db: AsyncSession, ciudad: CiudadCreate):
    query = text("CALL insertar_ciudad(:_nombre_ciudad, :_cod_departamento)")

    try:
        async with db.begin():
            await db.execute(query, {
                "_nombre_ciudad": ciudad.nombre_ciudad,
                "_cod_departamento": ciudad.cod_departamento
            })
        return {"message": f"Ciudad '{ciudad.nombre_ciudad}' insertada exitosamente"}
    except Exception as e:
        logger.error(f"Error al insertar ciudad: {e}")
        raise HTTPException(status_code=400, detail="No se pudo insertar la ciudad.")
    
async def modificar_ciudad(db: AsyncSession, cod_ciudad: int, ciudad: CiudadUpdate):
    # Verificar existencia antes de actualizar
    result = await db.execute(
        select(Ciudad).where(Ciudad.cod_ciudad == cod_ciudad)
    )
    existente = result.scalar_one_or_none()
    if not existente:
        raise HTTPException(status_code=404, detail=f"No se encontró la ciudad con ID {cod_ciudad}")

    query = text("CALL modificar_ciudad(:_cod_ciudad, :_nombre_ciudad, :_cod_departamento)")

    try:
        await db.execute(query, {
            "_cod_ciudad": cod_ciudad,
            "_nombre_ciudad": ciudad.nombre_ciudad,
            "_cod_departamento": ciudad.cod_departamento
        })
        await db.commit()
        return {"message": f"Ciudad con ID {cod_ciudad} modificada exitosamente"}
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=400, detail="No se pudo modificar la ciudad.")
    
async def eliminar_ciudad(db: AsyncSession, cod_ciudad: int):
    # Validar si la ciudad existe
    result = await db.execute(
        select(Ciudad).where(Ciudad.cod_ciudad == cod_ciudad)
    )
    existente = result.scalar_one_or_none()
    if not existente:
        raise HTTPException(status_code=404, detail=f"No se encontró la ciudad con ID {cod_ciudad}")

    query = text("CALL eliminar_ciudad(:_cod_ciudad)")

    try:
        await db.execute(query, {"_cod_ciudad": cod_ciudad})
        await db.commit()
        return {"message": f"Ciudad con ID {cod_ciudad} eliminada exitosamente"}
    except Exception as e:
        await db.rollback()
        error_str = str(e)

        if "en uso por" in error_str.lower():
            raise HTTPException(
                status_code=400,
                detail="Esta ciudad está en uso por una o más direcciones y no se puede eliminar."
            )

        raise HTTPException(status_code=500, detail="Error interno al eliminar la ciudad.")
    
def obtener_ciudades(
    db: Session,skip: int = 0,limit: int = 10) -> List[Ciudad]:
    return ( db.query(Ciudad).offset(skip).limit(limit).all())

def obtener_ciudad_por_id(db: Session,cod_ciudad: int) -> Ciudad:
    """
    Devuelve una ciudad por su ID.
    - cod_ciudad: ID de la ciudad a consultar
    """
    ciudad = (db.query(Ciudad).filter(Ciudad.cod_ciudad == cod_ciudad).first())

    if not ciudad:
        raise HTTPException( status_code=404,detail=f"No se encontró la ciudad con ID {cod_ciudad}")
    return ciudad

async def insertar_tipo_direccion(db: AsyncSession, tipo: TipoDireccionCreate):
    query = text("CALL insertar_tipo_direccion(:_nombre_tipo_direccion)")

    try:
        async with db.begin():
            await db.execute(query, {"_nombre_tipo_direccion": tipo.nombre_tipo_direccion})
        return {"message": f"Tipo de dirección '{tipo.nombre_tipo_direccion}' insertado exitosamente"}
    except Exception as e:
        logger.error(f"Error al insertar tipo de dirección: {e}")
        raise HTTPException(status_code=400, detail="No se pudo insertar el tipo de dirección.")
    
async def modificar_tipo_direccion(db: AsyncSession, cod_tipo_direccion: int, tipo: TipoDireccionUpdate):
    # Validar si existe
    result = await db.execute(
        select(TipoDireccion).where(TipoDireccion.cod_tipo_direccion == cod_tipo_direccion)
    )
    existente = result.scalar_one_or_none()
    if not existente:
        raise HTTPException(
            status_code=404,
            detail=f"No se encontró el tipo de dirección con ID {cod_tipo_direccion}"
        )

    query = text("CALL modificar_tipo_direccion(:_cod_tipo_direccion, :_nombre_tipo_direccion)")

    try:
        await db.execute(query, {
            "_cod_tipo_direccion": cod_tipo_direccion,
            "_nombre_tipo_direccion": tipo.nombre_tipo_direccion
        })
        await db.commit()
        return {"message": f"Tipo de dirección con ID {cod_tipo_direccion} modificado exitosamente"}
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=400, detail="No se pudo modificar el tipo de dirección.")
    
async def eliminar_tipo_direccion(db: AsyncSession, cod_tipo_direccion: int):
    # Validar si existe
    result = await db.execute(
        select(TipoDireccion).where(TipoDireccion.cod_tipo_direccion == cod_tipo_direccion)
    )
    existente = result.scalar_one_or_none()

    if not existente:
        raise HTTPException(
            status_code=404,
            detail=f"No se encontró el tipo de dirección con ID {cod_tipo_direccion}"
        )

    query = text("CALL eliminar_tipo_direccion(:_cod_tipo_direccion)")

    try:
        await db.execute(query, {"_cod_tipo_direccion": cod_tipo_direccion})
        await db.commit()
        return {"message": f"Tipo de dirección con ID {cod_tipo_direccion} eliminado exitosamente"}
    except Exception as e:
        await db.rollback()
        error_str = str(e)

        if "en uso por" in error_str.lower():
            raise HTTPException(
                status_code=400,
                detail="Este tipo de dirección está en uso por una o más direcciones y no se puede eliminar."
            )

        raise HTTPException(status_code=500, detail="Error interno al eliminar el tipo de dirección.")
    

def obtener_tipos_direccion(db: Session,skip: int = 0,limit: int = 10) -> List[TipoDireccion]:
    return ( db.query(TipoDireccion).offset(skip).limit(limit).all())

def obtener_tipo_direccion_por_id(db: Session,cod_tipo_direccion: int) -> TipoDireccion:
    """
    Devuelve un tipo de dirección por su ID.
    - cod_tipo_direccion: ID a consultar
    """
    tipo = (db.query(TipoDireccion).filter(TipoDireccion.cod_tipo_direccion == cod_tipo_direccion).first())

    if not tipo:
        raise HTTPException(status_code=404,detail=f"No se encontró el tipo de dirección con ID {cod_tipo_direccion}")
    return tipo

async def insertar_direccion(db: AsyncSession, direccion: DireccionCreate):
    query = text("""
        CALL insertar_direccion(
            :_cod_persona,
            :_cod_ciudad,
            :_cod_tipo_direccion,
            :_direccion1,
            :_direccion2,
            :_direccion3,
            :_estado_direccion
        )
    """)
    try:
        await db.execute(query, {
            "_cod_persona": direccion.cod_persona,
            "_cod_ciudad": direccion.cod_ciudad,
            "_cod_tipo_direccion": direccion.cod_tipo_direccion,
            "_direccion1": direccion.direccion1,
            "_direccion2": direccion.direccion2,
            "_direccion3": direccion.direccion3,
            "_estado_direccion": direccion.estado_direccion
        })
        await db.commit()
    except Exception as e:
        await db.rollback()
        raise e

async def actualizar_direccion_crud(db: AsyncSession, cod_direccion: int, direccion: DireccionUpdate):
    # Verificar existencia
    result = await db.execute(select(Direccion).where(Direccion.cod_direccion == cod_direccion))
    existe = result.scalar_one_or_none()
    if not existe:
        raise HTTPException(
            status_code=404,
            detail=f"No se encontró la dirección con ID {cod_direccion}"
        )

    query = text("""
        CALL actualizar_direccion(
            :_cod_direccion,
            :_cod_tipo_direccion,
            :_direccion1,
            :_direccion2,
            :_direccion3,
            :_estado_direccion
        )
    """)

    try:
        await db.execute(query, {
            "_cod_direccion": cod_direccion,
            "_cod_tipo_direccion": direccion.cod_tipo_direccion,
            "_direccion1": direccion.direccion1,
            "_direccion2": direccion.direccion2,
            "_direccion3": direccion.direccion3,
            "_estado_direccion": direccion.estado_direccion
        })
        await db.commit()
        return {"message": f"Dirección con ID {cod_direccion} actualizada correctamente"}
    except Exception as e:
        await db.rollback()
        raise

async def eliminar_direccion_crud(db: AsyncSession, cod_direccion: int):
    # Verificar existencia
    result = await db.execute(select(Direccion).where(Direccion.cod_direccion == cod_direccion))
    direccion = result.scalar_one_or_none()

    if not direccion:
        raise HTTPException(
            status_code=404,
            detail=f"No se encontró la dirección con ID {cod_direccion}"
        )

    query = text("CALL eliminar_direccion(:_cod_direccion)")

    try:
        await db.execute(query, {"_cod_direccion": cod_direccion})
        await db.commit()
        return {"message": f"Dirección con ID {cod_direccion} eliminada exitosamente"}
    except Exception as e:
        await db.rollback()
        raise

def obtener_direcciones(db: Session,skip: int = 0,limit: int = 10) -> List[Direccion]:
    return (db.query(Direccion).offset(skip).limit(limit).all())

def obtener_direccion_por_id(db: Session, cod_direccion: int) -> Direccion:
    direccion = (db.query(Direccion).filter(Direccion.cod_direccion == cod_direccion).first())

    if not direccion:
        raise HTTPException(status_code=404,detail=f"No se encontró la dirección con ID {cod_direccion}")
    return direccion

def obtener_direcciones_por_estado(db: Session,estado: str,skip: int = 0,limit: int = 10) -> List[Direccion]:
    return (db.query(Direccion).filter(Direccion.estado_direccion == estado).offset(skip).limit(limit).all())

def obtener_direcciones_por_persona(db: Session,cod_persona: int,skip: int = 0,limit: int = 10) -> List[Direccion]:
    return (db.query(Direccion).filter(Direccion.cod_persona == cod_persona).offset(skip).limit(limit).all())