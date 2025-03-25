from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from app.utils.utils import validar_tipo_modelo
from fastapi import HTTPException
from app.schemas.Seguridad.model_to_rol import AsignarRolRequest

# ✅ Asignar rol a modelo usando procedimiento almacenado
async def asignar_rol_a_modelo_crud(db: AsyncSession, datos: AsignarRolRequest):
    # 🔎 Validar si ya existe la asignación
    check_query = text("""
        SELECT 1 FROM model_has_roles
        WHERE role_id = :role_id AND model_type = :model_type AND model_id = :model_id
    """)

    result = await db.execute(check_query, {
        "role_id": datos.role_id,
        "model_type": datos.tipo_modelo,
        "model_id": datos.id_modelo
    })

    if result.scalar():
        raise HTTPException(
            status_code=409,
            detail="Este rol ya está asignado al modelo."
        )

    # ✅ Ejecutar el procedimiento almacenado
    insert_query = text("""
        CALL asignar_rol_a_modelo(:role_id, :model_type, :model_id)
    """)
    await db.execute(insert_query, {
        "role_id": datos.role_id,
        "model_type": datos.tipo_modelo,
        "model_id": datos.id_modelo
    })
    await db.commit()
    return {"message": "Rol asignado correctamente al modelo"}

# Revocar rol a modelo usando procedimiento almacenado
async def revocar_rol_de_modelo_crud(db: AsyncSession, datos: AsignarRolRequest):
    # Validar si la relación existe antes de intentar eliminar
    check_query = text("""
        SELECT 1 FROM model_has_roles
        WHERE role_id = :role_id AND model_type = :tipo_modelo AND model_id = :id_modelo
    """)
    result = await db.execute(check_query, {
        "role_id": datos.role_id,
        "tipo_modelo": datos.tipo_modelo,
        "id_modelo": datos.id_modelo
    })

    if not result.scalar():
        raise HTTPException(status_code=404, detail="El rol no está asignado al modelo indicado.")

    # Procedimiento almacenado
    delete_query = text("CALL revocar_rol_de_modelo(:role_id, :tipo_modelo, :id_modelo)")
    await db.execute(delete_query, datos.model_dump())
    await db.commit()
    return {"message": "Rol revocado correctamente del modelo"}


async def consultar_roles_por_modelo_crud(
    db: AsyncSession,
    tipo_modelo: str,
    id_modelo: int
):
    # Validación solo con regex
    validar_tipo_modelo(tipo_modelo)

    try:
        query = text(f"""
            SELECT r.id, r.name
            FROM model_has_roles mhr
            JOIN roles r ON mhr.role_id = r.id
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
                detail=f"No hay roles asignados para el modelo '{tipo_modelo}' con ID {id_modelo}."
            )

        return [dict(row._mapping) for row in rows]

    except HTTPException:
        raise

    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"Error al consultar roles del modelo: {str(e)}"
        )

async def consultar_modelos_por_rol_crud(db: AsyncSession, role_id: int):
    try:
        query = text("""
            SELECT model_type, model_id
            FROM model_has_roles
            WHERE role_id = :role_id
        """)

        result = await db.execute(query, {"role_id": role_id})
        rows = result.fetchall()

        if not rows:
            raise HTTPException(
                status_code=404,
                detail=f"No hay modelos asignados al rol con ID {role_id}."
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
            detail=f"Error al consultar modelos por rol: {str(e)}"
        )