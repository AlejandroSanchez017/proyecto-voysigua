from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session, joinedload
from sqlalchemy.sql import text, select
from app.schemas.Personas.empleados import (
    EmpleadoCreate, EmpleadoUpdate, NombreTipoEmpleadoCreate, 
    AreasCreate, TipoContratoCreate, EmpleadoDespedir
)
from app.models.Personas.empleados import Empleado, NombreTipoEmpleado, Areas, TipoContrato
import logging

logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)

# Insertar empleado llamando a procedimiento almacenado
async def insertar_empleado(db: AsyncSession, empleado: EmpleadoCreate):
    query = text("""
        CALL insertar_empleado(:cod_persona, :cod_tipo_empleado, :cod_area, :cod_tipo_contrato, 
                               :fecha_contratacion, :salario, :estado_empleado)
    """)
    try:
        async with db.begin():
            await db.execute(query, empleado.model_dump(exclude_unset=True))
            await db.commit()
    except Exception as e:
        logger.error(f"Error al insertar empleado: {str(e)}")
        await db.rollback()
        raise

# Insertar tipo de empleado
async def insertar_tipo_empleado(db: AsyncSession, tipo_empleado: NombreTipoEmpleadoCreate):
    nuevo_tipo = NombreTipoEmpleado(nombre_tipo_empleado=tipo_empleado.nombre_tipo_empleado)
    try:
        async with db.begin():
            db.add(nuevo_tipo)
            # NO hagas await db.commit() ni await db.rollback() dentro del with
        # Fuera del with, la transacción ya está confirmada si no hubo excepción

        # Si necesitas refrescar para obtener la PK recién generada:
        await db.refresh(nuevo_tipo)

        return nuevo_tipo
    except Exception as e:
        logger.error(f"Error al insertar tipo de empleado: {str(e)}")
        # El rollback automático ocurre si hay excepción dentro del with
        # Fuera del with, si quieres forzar un rollback adicional, puedes hacerlo,
        # pero no es habitual a menos que manejes la excepción manualmente.
        raise

# Obtener todos los tipos de empleado
async def obtener_tipos_empleado(db: AsyncSession):
    result = await db.execute(select(NombreTipoEmpleado))
    return result.scalars().all()

# Obtener empleado por ID
async def obtener_empleado_por_id(db: AsyncSession, cod_empleado: int):
    empleado = await db.get(Empleado, cod_empleado)
    return empleado if empleado else None

# Obtener todos los empleados con ORM
def obtener_todos_los_empleados(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Empleado)\
        .options(
            joinedload(Empleado.nombre_tipo_empleado), 
            joinedload(Empleado.nombre_area), 
            joinedload(Empleado.tipo_contrato)
        )\
        .offset(skip)\
        .limit(limit)\
        .all()

# Actualizar empleado
async def actualizar_empleado(db: AsyncSession, cod_empleado: int, empleado: EmpleadoUpdate):
    query = text("""
        CALL actualizar_empleado(:cod_empleado, :cod_persona, :cod_tipo_empleado, :cod_area, 
                                 :cod_tipo_contrato, :fecha_contratacion, :salario, :estado_empleado)
    """)
    try:
        async with db.begin():
            await db.execute(query, {"cod_empleado": cod_empleado, **empleado.model_dump(exclude_unset=True)})
            await db.commit()
    except Exception as e:
        logger.error(f"Error al actualizar empleado {cod_empleado}: {str(e)}")
        await db.rollback()
        raise
    
# Insertar área
async def insertar_area(db: AsyncSession, area: AreasCreate):
    nueva_area = Areas(nombre_area=area.nombre_area)
    try:
        async with db.begin():
            # Se inicia la transacción y se asegura commit/rollback automático
            db.add(nueva_area)
            # No hagas db.commit() ni db.rollback() aquí; el 'with' lo maneja.
        
        # Fuera del bloque, la transacción ya está “committed” si no hubo error.
        # Si necesitas refrescar el objeto para obtener datos recientes (p.ej. PK),
        # se puede hacer aquí:
        await db.refresh(nueva_area)

        return nueva_area
    except Exception as e:
        logger.error(f"Error al insertar área: {str(e)}")
        # Si quieres estar seguro, aunque el block above ya hace rollback en error:
        # await db.rollback()
        raise

# Obtener todas las areas
async def obtener_areas(db: AsyncSession):
    result = await db.execute(select(Areas).order_by(Areas.cod_area))
    return result.scalars().all()

# Eliminar área
async def eliminar_area(db: AsyncSession, cod_area: int):
    try:
        async with db.begin():
            result = await db.execute(select(Areas).filter_by(cod_area=cod_area))
            db_area = result.scalars().first()
            if not db_area:
                return None
            await db.delete(db_area)
            await db.commit()
            return db_area
    except Exception as e:
        logger.error(f"Error al eliminar área {cod_area}: {str(e)}")
        await db.rollback()
        raise

    # Insertar tipo de contrato
async def insertar_tipo_contrato(db: AsyncSession, tipo_contrato: TipoContratoCreate):
    nuevo_contrato = TipoContrato(tipo_contrato=tipo_contrato.tipo_contrato)
    try:
        async with db.begin():
            db.add(nuevo_contrato)
            # No hagas db.commit() ni db.rollback() aquí
            # El commit automático sucede al salir del with si no hubo error
        
        # Si necesitas el id recién generado, puedes hacer refresh fuera del with:
        await db.refresh(nuevo_contrato)

        return nuevo_contrato

    except Exception as e:
        logger.error(f"Error al insertar tipo de contrato: {str(e)}")
        # El rollback automático ocurre si hay excepción dentro del with
        raise

# Obtener tipos de contrato
async def obtener_tipos_contrato(db: AsyncSession):
    result = await db.execute(select(TipoContrato).order_by(TipoContrato.cod_tipo_contrato))
    return result.scalars().all()

# Eliminar tipo de contrato
async def eliminar_tipo_contrato(db: AsyncSession, cod_tipo_contrato: int):
    try:
        async with db.begin():
            result = await db.execute(select(TipoContrato).filter_by(cod_tipo_contrato=cod_tipo_contrato))
            db_tipo_contrato = result.scalars().first()
            if not db_tipo_contrato:
                return None
            await db.delete(db_tipo_contrato)
            await db.commit()
            return db_tipo_contrato
    except Exception as e:
        logger.error(f"Error al eliminar tipo de contrato {cod_tipo_contrato}: {str(e)}")
        await db.rollback()
        raise

# Despedir empleado
async def despedir_empleado_crud(db: AsyncSession, cod_empleado: int, datos: EmpleadoDespedir):
    query = text("CALL despedir_empleado(:cod_empleado, :fecha_salida, :motivo_salida)")
    try:
        async with db.begin():
            await db.execute(query, {
                "cod_empleado": cod_empleado,
                "fecha_salida": datos.fecha_salida,
                "motivo_salida": datos.motivo_salida
            })
            await db.commit()
        return {"message": f"Empleado con ID {cod_empleado} ha sido despedido exitosamente"}
    except Exception as e:
        logger.error(f"Error al despedir empleado {cod_empleado}: {str(e)}")
        await db.rollback()
        raise
    
# Eliminar empleado
async def eliminar_empleado(db: AsyncSession, cod_empleado: int):
    try:
        async with db.begin():
            result = await db.execute(select(Empleado).filter_by(cod_empleado=cod_empleado))
            db_empleado = result.scalars().first()
            if not db_empleado:
                return None
            await db.delete(db_empleado)
            await db.commit()
            return db_empleado
    except Exception as e:
        logger.error(f"Error al eliminar empleado {cod_empleado}: {str(e)}")
        await db.rollback()
        raise

async def eliminar_tipo_empleado(db: AsyncSession, cod_tipo_empleado: int):
    try:
        async with db.begin():
            result = await db.execute(select(NombreTipoEmpleado).filter_by(cod_tipo_empleado=cod_tipo_empleado))
            tipo_empleado = result.scalars().first()
            if not tipo_empleado:
                return None
            await db.delete(tipo_empleado)
            await db.commit()
            return tipo_empleado
    except Exception as e:
        logger.error(f"Error al eliminar tipo de empleado {cod_tipo_empleado}: {str(e)}")
        await db.rollback()
        raise



