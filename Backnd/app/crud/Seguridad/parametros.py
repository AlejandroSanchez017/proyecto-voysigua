from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from app.schemas.Seguridad.parametros import ParametroCreate, ParametroUpdate, ParametroResponse
import logging

logger = logging.getLogger(__name__)

async def insertar_parametro(db: AsyncSession, parametro: ParametroCreate):
    query = text("""
        CALL insertar_parametro(:parametro, :valor, :descripcion, :categoria, :estado)
    """)

    try:
        async with db.begin():
            await db.execute(query, {
                "parametro": parametro.parametro,
                "valor": parametro.valor,
                "descripcion": parametro.descripcion,
                "categoria": parametro.categoria,
                "estado": parametro.estado
            })
        await db.commit()

        return {"message": f"Parámetro '{parametro.parametro}' insertado correctamente"}

    except Exception as e:
        logger.error(f"Error al insertar parámetro: {e}")
        raise

async def actualizar_parametro(db: AsyncSession, id: int, parametro: ParametroUpdate):
    data = parametro.dict(exclude_unset=True)

    query = text("""
        CALL actualizar_parametro(:id, :parametro, :valor, :descripcion, :categoria, :estado)
    """)

    try:
        async with db.begin():
            await db.execute(query, {
                "id": id,
                "parametro": data.get("parametro"),
                "valor": data.get("valor"),
                "descripcion": data.get("descripcion"),
                "categoria": data.get("categoria"),
                "estado": data.get("estado", "activo")
            })
        await db.commit()

        return {"message": f"Parámetro con ID {id} actualizado correctamente"}

    except Exception as e:
        logger.error(f"Error al actualizar parámetro: {e}")
        raise
    
async def inactivar_parametro(db: AsyncSession, id: int):
    query = text("""
        CALL inactivar_parametro(:id)
    """)

    try:
        async with db.begin():
            await db.execute(query, {"id": id})
        await db.commit()

        return {"message": f"Parámetro con ID {id} inactivado correctamente"}

    except Exception as e:
        logger.error(f"Error al inactivar parámetro: {e}")
        raise    

async def consultar_parametro_por_id(db: AsyncSession, id: int) -> ParametroResponse:
    query = text("""
        SELECT id, parametro, valor, descripcion, estado, categoria
        FROM parametros
        WHERE id = :id
    """)

    try:
        result = await db.execute(query, {"id": id})
        row = result.fetchone()

        if not row:
            raise ValueError(f"No se encontró el parámetro con ID {id}")

        return ParametroResponse(
            id=row[0],
            parametro=row[1],
            valor=row[2],
            descripcion=row[3],
            estado=row[4],
            categoria=row[5]
        )

    except Exception as e:
        logger.error(f"Error al consultar parámetro por ID: {e}")
        raise    

async def consultar_todos_parametros(db: AsyncSession) -> list[ParametroResponse]:
    query = text("""
        SELECT id, parametro, valor, descripcion, estado, categoria
        FROM parametros
    """)

    try:
        result = await db.execute(query)
        rows = result.fetchall()

        return [
            ParametroResponse(
                id=row[0],
                parametro=row[1],
                valor=row[2],
                descripcion=row[3],
                estado=row[4],
                categoria=row[5]
            )
            for row in rows
        ]
    except Exception as e:
        logger.error(f"Error al consultar todos los parámetros: {e}")
        raise    

async def consultar_parametros_por_estado(db: AsyncSession, estado: str) -> list[ParametroResponse]:
    query = text("""
        SELECT id, parametro, valor, descripcion, estado, categoria
        FROM parametros
        WHERE estado = :estado
    """)

    try:
        result = await db.execute(query, {"estado": estado})
        rows = result.fetchall()

        if not rows:
            raise ValueError(f"No se encontraron parámetros con estado '{estado}'.")

        return [
            ParametroResponse(
                id=row[0],
                parametro=row[1],
                valor=row[2],
                descripcion=row[3],
                estado=row[4],
                categoria=row[5]
            )
            for row in rows
        ]
    except Exception as e:
        logger.error(f"Error al consultar parámetros por estado: {e}")
        raise

async def consultar_parametros_por_categoria(db: AsyncSession, categoria: str) -> list[ParametroResponse]:
    query = text("""
        SELECT id, parametro, valor, descripcion, estado, categoria
        FROM parametros
        WHERE categoria = :categoria
    """)

    try:
        result = await db.execute(query, {"categoria": categoria})
        rows = result.fetchall()

        if not rows:
            raise ValueError(f"No se encontraron parámetros en la categoría '{categoria}'.")

        return [
            ParametroResponse(
                id=row[0],
                parametro=row[1],
                valor=row[2],
                descripcion=row[3],
                estado=row[4],
                categoria=row[5]
            )
            for row in rows
        ]
    except Exception as e:
        logger.error(f"Error al consultar parámetros por categoría: {e}")
        raise
