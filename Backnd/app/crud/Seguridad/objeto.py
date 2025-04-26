
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from fastapi import HTTPException
from app.models.Seguridad.objeto import Objetos
from app.schemas.Seguridad.objeto import ObjetoCreate, ObjetoUpdate, ObjetoResponse
import logging

logger = logging.getLogger(__name__)

async def insertar_objeto(db: AsyncSession, objeto: ObjetoCreate):
    query = text("""
        CALL insertar_objeto(:objeto, :descripcion, :status)
    """)

    try:
        async with db.begin():
            await db.execute(query, {"objeto": objeto.objeto, "descripcion": objeto.descripcion,
            "status": objeto.status})
        await db.commit()

        return {"message": f"Objeto insertado exitosamente: {objeto.objeto}"}
    
    except Exception as e:
        logger.error(f"Error al insertar objeto: {e}")
        raise


async def actualizar_objeto(db: AsyncSession, id: int, objeto: ObjetoUpdate):
    objeto_data = objeto.dict(exclude_unset=True)

    query = text("""
        CALL actualizar_objeto(:id, :objeto, :descripcion, :status)
    """)

    try:
        async with db.begin():
            await db.execute(query, {
                "id": id,
                "objeto": objeto_data.get("objeto"),
                "descripcion": objeto_data.get("descripcion"),
                "status": objeto_data.get("status")
            })
        await db.commit()

        return {"message": f"Objeto con ID {id} actualizado correctamente"}

    except Exception as e:
        logger.error(f"Error al actualizar objeto: {e}")
        raise

async def eliminar_objeto(db: AsyncSession, id: int):
    query = text("""
        CALL eliminar_objeto(:id)
    """)

    try:
        async with db.begin():
            await db.execute(query, {"id": id})
        await db.commit()
        return {"message": f"Objeto con ID {id} eliminado correctamente"}

    except Exception as e:
        logger.error(f"Error al eliminar objeto: {e}")
        raise

async def consultar_objeto_por_id(db: AsyncSession, id: int) -> ObjetoResponse:
    query = text("""
        SELECT id, objeto, descripcion, status
        FROM objetos
        WHERE id = :id
    """)

    try:
        result = await db.execute(query, {"id": id})
        row = result.fetchone()

        if not row:
            raise ValueError(f"No se encontró el objeto con ID {id}")

        return ObjetoResponse(
            id=row[0],
            objeto=row[1],
            descripcion=row[2],
            status=row[3]
        )

    except Exception as e:
        logger.error(f"Error al consultar objeto por ID: {e}")
        raise

async def consultar_todos_objetos(db: AsyncSession) -> list[ObjetoResponse]:
    query = text("""
        SELECT id, objeto, descripcion, status
        FROM objetos
    """)

    try:
        result = await db.execute(query)
        rows = result.fetchall()

        return [
            ObjetoResponse(
                id=row[0],
                objeto=row[1],
                descripcion=row[2],
                status=row[3]
            )
            for row in rows
        ]

    except Exception as e:
        logger.error(f"Error al consultar todos los objetos: {e}")
        raise    