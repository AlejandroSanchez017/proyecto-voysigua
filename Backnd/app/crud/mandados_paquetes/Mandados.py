from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from sqlalchemy.sql import select, text
from app.models.mandados_paquetes.mandados import Mandado
from app.schemas.mandados_paquetes.mandados import MandadoCreate, MandadoUpdate

async def insertar_mandado_crud_async(db: AsyncSession, mandado: MandadoCreate):
    query = text("""
        CALL insertar_mandado(
            :cod_persona, :tipo_pago_id, :cod_tipo_mandado, :cod_estado_mandado,
            :cuadre_motorista_id, :fecha, :cliente, :descripcion, :detalles,
            :total, :costo_base, :costo_extra, :hora_inicio, :hora_fin
        )
    """)
    await db.execute(query, mandado.model_dump())
    await db.commit()
    return {"message": "Mandado insertado exitosamente."}

async def actualizar_mandado_crud_async(db: AsyncSession, mandado: MandadoUpdate):
    query = text("""
        CALL actualizar_mandado(
            :cod_mandado, :cod_persona, :tipo_pago_id, :cod_tipo_mandado, :cod_estado_mandado,
            :cuadre_motorista_id, :fecha, :cliente, :descripcion, :detalles,
            :total, :costo_base, :costo_extra, :hora_inicio, :hora_fin
        )
    """)
    await db.execute(query, mandado.model_dump())
    await db.commit()
    return {"message": "Mandado actualizado exitosamente."}

async def eliminar_mandado_crud_async(db: AsyncSession, cod_mandado: int):
    query = text("CALL eliminar_mandado(:cod_mandado)")
    await db.execute(query, {"cod_mandado": cod_mandado})
    await db.commit()
    return {"message": "Mandado eliminado exitosamente."}

async def obtener_mandados_crud_async(db: AsyncSession, skip: int = 0, limit: int = 10):
    result = await db.execute(
        select(Mandado).order_by(Mandado.cod_mandado.desc()).offset(skip).limit(limit)
    )
    return result.scalars().all() 
    

