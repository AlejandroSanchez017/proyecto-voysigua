from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from sqlalchemy import text
from app.utils.utils import validar_tipo_modelo, extraer_campo_foreign_key
from app.schemas.Seguridad.model_to_permission import AsignarPermisoRequest
import logging

logger = logging.getLogger(__name__)


async def asignar_permiso_a_modelo_crud(db: AsyncSession, datos: AsignarPermisoRequest):
    # Validar si ya existe la asignación
    check_query = text("""
        SELECT 1 FROM model_has_permissions
        WHERE permission_id = :permission_id AND model_type = :model_type AND model_id = :model_id
    """)

    result = await db.execute(check_query, {
        "permission_id": datos.permission_id,
        "model_type": datos.tipo_modelo,
        "model_id": datos.id_modelo
    })

    if result.scalar():
        raise HTTPException(
            status_code=409,
            detail="Este permiso ya está asignado al modelo."
        )

    try:
        insert_query = text("""
            CALL asignar_permiso_a_modelo(:permission_id, :model_type, :model_id)
        """)
        await db.execute(insert_query, {
            "permission_id": datos.permission_id,
            "model_type": datos.tipo_modelo,
            "model_id": datos.id_modelo
        })
        await db.commit()
        return {"message": "Permiso asignado correctamente al modelo"}

    except IntegrityError as e:
        await db.rollback()
        error_msg = str(e.orig) if hasattr(e, "orig") else str(e)

        if "foreign key" in error_msg.lower() or "llave foránea" in error_msg.lower():
            campo = extraer_campo_foreign_key(error_msg)
            raise HTTPException(
                status_code=400,
                detail=f"El valor ingresado para '{campo}' no existe en la base de datos."
            )

        raise HTTPException(status_code=400, detail="Error de integridad en la base de datos.")

    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=400, detail=f"Error al asignar permiso: {str(e)}")
    
async def revocar_permiso_de_modelo_crud(
    db: AsyncSession,
    datos: AsignarPermisoRequest
):
    try:
        # Verificar si existe la asignación antes de intentar eliminarla
        check_query = text("""
            SELECT 1 FROM model_has_permissions
            WHERE permission_id = :permission_id AND model_type = :model_type AND model_id = :model_id
        """)
        result = await db.execute(check_query, {
            "permission_id": datos.permission_id,
            "model_type": datos.tipo_modelo,
            "model_id": datos.id_modelo
        })

        if not result.scalar():
            raise HTTPException(
                status_code=404,
                detail="Este permiso no está asignado al modelo."
            )

        # Llamar al procedimiento para revocar
        delete_query = text("""
            CALL revocar_permiso_de_modelo(:permission_id, :model_type, :model_id)
        """)
        await db.execute(delete_query, {
            "permission_id": datos.permission_id,
            "model_type": datos.tipo_modelo,
            "model_id": datos.id_modelo
        })

        await db.commit()
        return {"message": "Permiso revocado correctamente del modelo."}

    except HTTPException:
        raise  # ← Importante: no modificar si ya es una excepción HTTP personalizada

    except IntegrityError as e:
        error_msg = str(e.orig) if hasattr(e, "orig") else str(e)
        logger.error(f"Error de integridad al revocar permiso: {error_msg}")

        if "foreign key" in error_msg.lower() or "llave foránea" in error_msg.lower():
            campo = extraer_campo_foreign_key(error_msg)
            raise HTTPException(
                status_code=400,
                detail=f"El valor ingresado para '{campo}' no existe en la base de datos."
            )

        raise HTTPException(status_code=400, detail="Error de integridad en la base de datos.")

    except Exception as e:
        logger.error(f"Error general al revocar permiso: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
    
async def consultar_permisos_por_modelo_crud(
    db: AsyncSession,
    tipo_modelo: str,
    id_modelo: int
):
    validar_tipo_modelo(tipo_modelo)

    try:
        query = text("""
            SELECT DISTINCT p.id, p.name, p.guard_name
            FROM model_has_roles mhr
            JOIN role_has_permissions rhp ON mhr.role_id = rhp.role_id
            JOIN permissions p ON rhp.permission_id = p.id
            WHERE mhr.model_type = :tipo_modelo
              AND mhr.model_id = :id_modelo
        """)

        result = await db.execute(query, {
            "tipo_modelo": tipo_modelo,
            "id_modelo": id_modelo
        })

        rows = result.fetchall()

        if not rows:
            raise HTTPException(
                status_code=404,
                detail=f"No hay permisos asignados para el modelo '{tipo_modelo}' con ID {id_modelo}."
            )

        return [dict(row._mapping) for row in rows]

    except HTTPException:
        raise

    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"Error al consultar permisos del modelo: {str(e)}"
        )

    
async def consultar_modelos_por_permiso_crud(
    db: AsyncSession,
    permission_id: int
):
    try:
        query = text("""
            SELECT model_type, model_id
            FROM model_has_permissions
            WHERE permission_id = :permission_id
        """)

        result = await db.execute(query, {"permission_id": permission_id})
        rows = result.fetchall()

        if not rows:
            raise HTTPException(
                status_code=404,
                detail=f"No hay modelos asignados al permiso con ID {permission_id}."
            )

        # Validamos los tipos de modelo en cada resultado
        modelos = []
        for row in rows:
            tipo_modelo = row._mapping["model_type"]
            validar_tipo_modelo(tipo_modelo)
            modelos.append(dict(row._mapping))

        return modelos

    except HTTPException:
        raise

    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"Error al consultar modelos por permiso: {str(e)}"
        )
    
