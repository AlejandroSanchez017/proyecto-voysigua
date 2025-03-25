from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import text
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from app.models.Seguridad.roles import Role
from app.models.Seguridad.permisos import Permission
import logging

logger = logging.getLogger(__name__)

async def asignar_permiso_a_rol_crud(db: AsyncSession, permission_id: int, role_id: int):
    # 1) Verificar si ya existe la asignación
    check_query = text("""
        SELECT 1 
        FROM role_has_permissions
        WHERE permission_id = :perm_id
          AND role_id = :role_id
    """)
    check_result = await db.execute(check_query, {"perm_id": permission_id, "role_id": role_id})
    if check_result.scalar():
        raise ValueError(f"El rol con ID {role_id} ya tiene asignado el permiso con ID {permission_id}.")
    
    # 2) Verificar si existe el permiso
    perm_query = text("SELECT 1 FROM permissions WHERE id = :pid")
    perm_result = await db.execute(perm_query, {"pid": permission_id})
    if not perm_result.scalar():
        raise ValueError(f"No existe el permiso con ID {permission_id}")

    # 3) Verificar si existe el rol
    role_query = text("SELECT 1 FROM roles WHERE id = :rid")
    role_result = await db.execute(role_query, {"rid": role_id})
    if not role_result.scalar():
        raise ValueError(f"No existe el rol con ID {role_id}")

    # 4) Llamar al procedure de asignación de permiso
    query = text("CALL asignar_permiso_a_rol(:permission_id, :role_id)")
    try:
        await db.execute(query, {"permission_id": permission_id, "role_id": role_id})
        await db.commit()
        return {"message": f"Permiso con ID {permission_id} asignado al rol con ID {role_id}"}
    except Exception as e:
        await db.rollback()
        raise

async def revocar_permiso_de_rol_crud(db: AsyncSession, permission_id: int, role_id: int):
    # 1) Verificar si existe la asignación (permission_id, role_id)
    check_query = text("""
        SELECT 1
        FROM role_has_permissions
        WHERE permission_id = :perm_id
          AND role_id = :role_id
    """)
    check_result = await db.execute(check_query, {"perm_id": permission_id, "role_id": role_id})
    if not check_result.scalar():
        # No existe la asignación
        raise ValueError(f"No existe la asignación del permiso con ID {permission_id} para el rol con ID {role_id}.")

    # 2) Llamar al procedure de revocar
    query = text("CALL revocar_permiso_de_rol(:permission_id, :role_id)")
    try:
        await db.execute(query, {"permission_id": permission_id, "role_id": role_id})
        await db.commit()
        return {"message": f"Permiso con ID {permission_id} revocado del rol con ID {role_id}"}
    except Exception as e:
        await db.rollback()
        raise

async def obtener_permisos_de_rol(db: AsyncSession, role_id: int):
    stmt = (
        select(Role)
        .options(selectinload(Role.permissions))
        .where(Role.id == role_id)
    )
    result = await db.execute(stmt)
    role_obj = result.scalars().first()
    if not role_obj:
        return None
    return role_obj.permissions

async def obtener_roles_de_permiso(db: AsyncSession, permission_id: int):
    stmt = (
        select(Permission)
        .options(selectinload(Permission.roles))
        .where(Permission.id == permission_id)
    )
    result = await db.execute(stmt)
    perm_obj = result.scalars().first()
    if not perm_obj:
        return None
    return perm_obj.roles