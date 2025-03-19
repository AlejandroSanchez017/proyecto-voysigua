from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import text
from sqlalchemy import select
from app.schemas.Seguridad.permisos import PermisoCreate, PermisoUpdate
from app.models.Seguridad.permisos import Permission
import logging

logger = logging.getLogger(__name__)

# Insertar permiso: llama al procedure insertar_permiso
async def insertar_permiso(db: AsyncSession, permiso: PermisoCreate):
    query = text("""
        CALL insertar_permiso(:name, :guard_name)
    """)
    try:
        async with db.begin():
            await db.execute(query, {"name": permiso.name, "guard_name": permiso.guard_name})
        return {"message": f"Permiso insertado exitosamente: {permiso.name}"}
    except Exception as e:
        logger.error(f"Error al insertar permiso: {e}")
        raise

# Actualizar permiso: llama al procedure actualizar_permiso, que verifica si se actualizó
async def actualizar_permiso(db: AsyncSession, permiso_id: int, permiso: PermisoUpdate):
    query = text("""
        CALL actualizar_permiso(:id, :name, :guard_name)
    """)
    try:
        async with db.begin():
            await db.execute(query, {"id": permiso_id, "name": permiso.name, "guard_name": permiso.guard_name})
        return {"message": f"Permiso con ID {permiso_id} actualizado exitosamente"}
    except Exception as e:
        logger.error(f"Error al actualizar permiso con ID {permiso_id}: {e}")
        raise

# Eliminar permiso: llama al procedure eliminar_permiso, que verifica si se eliminó
async def eliminar_permiso(db: AsyncSession, permiso_id: int):
    query = text("""
        CALL eliminar_permiso(:id)
    """)
    try:
        async with db.begin():
            await db.execute(query, {"id": permiso_id})
        return {"message": f"Permiso con ID {permiso_id} eliminado exitosamente"}
    except Exception as e:
        logger.error(f"Error al eliminar permiso con ID {permiso_id}: {e}")
        raise

# Para consultar, en vez de llamar a un procedure que solo emite NOTICE, se recomienda hacer SELECT
async def obtener_todos_los_permisos(db: AsyncSession):
    result = await db.execute(select(Permission))
    return result.scalars().all()

async def obtener_permiso_por_id(db: AsyncSession, permiso_id: int):
    query = text("SELECT id, name, guard_name FROM permissions WHERE id = :id")
    result = await db.execute(query, {"id": permiso_id})
    permiso = result.mappings().first()
    return permiso
