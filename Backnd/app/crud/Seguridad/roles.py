from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import text
from sqlalchemy import select
from app.schemas.Seguridad.roles import RoleCreate, RoleUpdate
from app.models.Seguridad.roles import Role
import logging

logger = logging.getLogger(__name__)

async def insertar_rol(db: AsyncSession, role: RoleCreate):
    """
    Llama al stored procedure 'insertar_rol'
    que inserta un rol en la tabla 'roles'.
    """
    query = text("CALL insertar_rol(:name, :guard_name, :status)")

    try:
        # Manejamos la transacción con 'async with db.begin()'
        async with db.begin():
            await db.execute(
                query,
                {
                    "name": role.name,
                    "guard_name": role.guard_name,
                    "status": role.status
                }
            )
            # ¡No hagas db.commit() dentro de un 'with db.begin()'!
            # Se hace commit automático al salir del bloque
        # Al llegar aquí, ya se hizo commit sin excepción
        return {"message": f"Rol '{role.name}' insertado exitosamente"}
    except Exception as e:
        logger.error(f"Error al insertar rol: {e}")
        # Se hace rollback automático si ocurre excepción dentro del with
        raise

async def obtener_todas_los_roles(db: AsyncSession):
    result = await db.execute(select(Role))
    return result.scalars().all()

async def actualizar_rol(db: AsyncSession, role_id: int, new_data: RoleUpdate):
    """
    Llama al stored procedure 'actualizar_rol(_id, _name, _guard_name, _status)' 
    para actualizar un rol existente.
    """
    query = text("CALL actualizar_rol(:id, :name, :guard_name, :status)")
    try:
        async with db.begin():
            await db.execute(
                query,
                {
                    "id": role_id,
                    "name": new_data.name,
                    "guard_name": new_data.guard_name,
                    "status": new_data.status
                }
            )
        return {"message": f"Rol con ID {role_id} actualizado exitosamente"}
    except Exception as e:
        logger.error(f"Error al actualizar rol {role_id}: {e}")
        # Se hace rollback automático si ocurre excepción dentro del with
        raise

async def eliminar_rol(db: AsyncSession, role_id: int):
    """
    Llama al stored procedure 'eliminar_rol(_id)' para borrar un rol en la BD.
    """
    query = text("CALL eliminar_rol(:id)")
    try:
        async with db.begin():
            await db.execute(query, {"id": role_id})
        return {"message": f"Rol con ID {role_id} eliminado exitosamente"}
    except Exception as e:
        logger.error(f"Error al eliminar rol {role_id}: {e}")
        raise

async def buscar_rol_por_id(db: AsyncSession, role_id: int):
    """
    1) Llama al stored procedure 'buscar_rol_por_id(_id)'
       (esto solo hará el RAISE NOTICE en el servidor).
    2) Luego hace un SELECT para obtener la fila y
       retornarla a la API.
    """
    # 1) Llamada al procedure (no retorna datos directos, solo logs)
    proc_query = text("CALL buscar_rol_por_id(:id)")
    try:
        async with db.begin():
            await db.execute(proc_query, {"id": role_id})
        # Se hace commit al salir del bloque sin excepción
    except Exception as e:
        logger.error(f"Error al ejecutar 'buscar_rol_por_id' para ID {role_id}: {e}")
        raise

    # 2) Hacer un SELECT para obtener los datos reales de la tabla
    try:
        # Abre otra transacción o reusa la conexión
        result = await db.execute(
            text("SELECT id, name, guard_name, status FROM roles WHERE id = :id"),
            {"id": role_id}
        )
        row = result.mappings().first()
        if not row:
            return None  # Indica que no existe
        return {
            "id": row["id"],
            "name": row["name"],
            "guard_name": row["guard_name"],
            "status": row["status"]
        }
    except Exception as e:
        logger.error(f"Error al SELECT rol {role_id}: {e}")
        raise