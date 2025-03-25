from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_async_db
from sqlalchemy import text
from typing import List
from app.crud.Seguridad.role_permissions import asignar_permiso_a_rol_crud, revocar_permiso_de_rol_crud, obtener_permisos_de_rol, obtener_roles_de_permiso
from app.schemas.Seguridad.role_permissions import AssignPermissionToRole, PermissionResponse, RoleResponse
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

@router.post("/role-permissions/assign", response_model=dict)
async def assign_permission_to_role(
    data: AssignPermissionToRole,
    db: AsyncSession = Depends(get_async_db)
):
    try:
        result = await asignar_permiso_a_rol_crud(db, data.permission_id, data.role_id)
        return result
    except ValueError as ve:
        # Si se lanza ValueError por asignación duplicada o por no existencia, devuelve 404 o 409
        raise HTTPException(status_code=404, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/rol-permissions", response_model=list[dict])
async def obtener_roles_con_permisos(db: AsyncSession = Depends(get_async_db)):
    query = text("SELECT * FROM role_has_permissions")
    result = await db.execute(query)
    rows = result.fetchall()

    # Convertimos los resultados a lista de diccionarios
    return [dict(row._mapping) for row in rows]
    
@router.delete("/role-permissions/revoke", response_model=dict)
async def revoke_permission(
    data: AssignPermissionToRole, 
    db: AsyncSession = Depends(get_async_db)
):
    try:
        result = await revocar_permiso_de_rol_crud(db, data.permission_id, data.role_id)
        return result
    except ValueError as ve:
        # Mensaje amigable, por ejemplo 404
        raise HTTPException(status_code=404, detail=str(ve))
    except Exception as e:
        # Otros errores
        raise HTTPException(status_code=400, detail=str(e))
    
@router.get("/role-permissions/{role_id}/permisos", response_model=List[PermissionResponse])
async def get_permisos_por_rol(role_id: int, db: AsyncSession = Depends(get_async_db)):
    permisos = await obtener_permisos_de_rol(db, role_id)
    if not permisos:
        # Si no hay permisos o no existe el rol, podrías decidir si devuelves []
        # o un 404. Aquí un ejemplo con 404 si no hay nada.
        raise HTTPException(status_code=404, detail=f"No hay permisos asignados al rol con ID {role_id}")
    return permisos

@router.get("/permissions/{permission_id}/roles", response_model=List[RoleResponse])
async def get_roles_por_permiso(permission_id: int, db: AsyncSession = Depends(get_async_db)):
    """
    Retorna la lista de roles asociados a un permiso, usando eager loading.
    """
    roles = await obtener_roles_de_permiso(db, permission_id)
    if roles is None:
        raise HTTPException(status_code=404, detail=f"No existe el permiso con ID {permission_id}")
    if not roles:
        raise HTTPException(status_code=404, detail=f"No hay roles asignados al permiso con ID {permission_id}")
    return roles
