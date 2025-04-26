from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session, joinedload
from sqlalchemy.sql import text, select
from typing import List
from fastapi import HTTPException
from app.schemas.Personas.empleados import (
    EmpleadoCreate, EmpleadoUpdate, NombreTipoEmpleadoCreate, 
    AreasCreate, TipoContratoCreate, EmpleadoDespedir, MarcaCreate, MarcaUpdate, TipoTransporteCreate, TipoTransporteUpdate,
    VehiculoMotoristaCreate, VehiculoMotoristaUpdate
)
from app.models.Personas.empleados import (Empleado, NombreTipoEmpleado, Areas, TipoContrato, Marca, TipoTransporte,
                                           VehiculoMotorista)
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
        await db.execute(query, empleado.model_dump(exclude_unset=True))
        await db.commit()  # commit manual
    except Exception as e:
        await db.rollback()
        logger.error(f"Error al insertar empleado: {str(e)}")
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
async def actualizar_empleado_crud(db: AsyncSession, cod_empleado: int, empleado: EmpleadoUpdate):
    query = text("""
        CALL actualizar_empleado(
            :cod_empleado,
            :cod_persona,
            :cod_tipo_empleado,
            :cod_area,
            :cod_tipo_contrato,
            :fecha_salida,
            :motivo_salida,
            :fecha_contratacion,
            :salario,
            :estado_empleado
        )
    """)
    try:
        await db.execute(
            query,
            {
                "cod_empleado": cod_empleado,
                **empleado.model_dump(exclude_unset=True)
            }
        )
        await db.commit()
        return {"message": f"Empleado con ID {cod_empleado} actualizado correctamente"}
    except Exception as e:
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

async def insertar_marca(db: AsyncSession, marca: MarcaCreate):
    query = text("CALL insertar_marca(:_nombre_marca)")

    try:
        async with db.begin():
            await db.execute(query, {"_nombre_marca": marca.nombre_marca})
        return {"message": f"Marca '{marca.nombre_marca}' insertada exitosamente"}
    except Exception as e:
        logger.error(f"Error al insertar marca: {e}")
        raise HTTPException(status_code=400, detail="No se pudo insertar la marca.")
    
async def modificar_marca(db: AsyncSession, cod_marca: int, marca: MarcaUpdate):
    # Verificar si existe
    result = await db.execute(
        select(Marca).where(Marca.cod_marca == cod_marca)
    )
    existente = result.scalar_one_or_none()
    if not existente:
        raise HTTPException(status_code=404, detail=f"No se encontró la marca con ID {cod_marca}")

    query = text("CALL modificar_marca(:_cod_marca, :_nombre_marca)")

    try:
        await db.execute(query, {
            "_cod_marca": cod_marca,
            "_nombre_marca": marca.nombre_marca
        })
        await db.commit()
        return {"message": f"Marca con ID {cod_marca} modificada exitosamente"}
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=400, detail="No se pudo modificar la marca.")
    
async def eliminar_marca(db: AsyncSession, cod_marca: int):
    # Verificar si la marca existe
    result = await db.execute(
        select(Marca).where(Marca.cod_marca == cod_marca)
    )
    existente = result.scalar_one_or_none()

    if not existente:
        raise HTTPException(
            status_code=404,
            detail=f"No se encontró la marca con ID {cod_marca}"
        )

    query = text("CALL eliminar_marca(:_cod_marca)")

    try:
        await db.execute(query, {"_cod_marca": cod_marca})
        await db.commit()
        return {"message": f"Marca con ID {cod_marca} eliminada exitosamente"}
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail="Error interno al eliminar la marca.")

def obtener_marcas(
    db: Session, skip: int = 0, limit: int = 10
) -> List[Marca]:
    """
    Devuelve una lista de marcas paginada.
    - skip: cuántos registros omitir
    - limit: cuántos registros devolver como máximo
    """
    return (
        db.query(Marca).offset(skip).limit(limit).all()
    )

def obtener_marca_por_id(
    db: Session, cod_marca: int
) -> Marca:
    """
    Devuelve una marca por su ID.
    - cod_marca: ID de la marca a consultar
    """
    marca = (
        db.query(Marca).filter(Marca.cod_marca == cod_marca).first()
    )

    if not marca:
        raise HTTPException(
            status_code=404,
            detail=f"No se encontró la marca con ID {cod_marca}"
        )

    return marca

async def insertar_tipo_transporte(db: AsyncSession, tipo: TipoTransporteCreate):
    query = text("CALL insertar_tipo_transporte(:_nombre_tipo_transporte)")

    try:
        async with db.begin():
            await db.execute(query, {"_nombre_tipo_transporte": tipo.nombre_tipo_transporte})
        return {"message": f"Tipo de transporte '{tipo.nombre_tipo_transporte}' insertado exitosamente"}
    except Exception as e:
        logger.error(f"Error al insertar tipo de transporte: {e}")
        raise HTTPException(status_code=400, detail="No se pudo insertar el tipo de transporte.")
    
async def modificar_tipo_transporte(db: AsyncSession, cod_tipo_transporte: int, tipo: TipoTransporteUpdate):
    # Verificar si existe
    result = await db.execute(
        select(TipoTransporte).where(TipoTransporte.cod_tipo_transporte == cod_tipo_transporte)
    )
    existente = result.scalar_one_or_none()
    if not existente:
        raise HTTPException(
            status_code=404,
            detail=f"No se encontró el tipo de transporte con ID {cod_tipo_transporte}"
        )

    query = text("CALL modificar_tipo_transporte(:_cod_tipo_transporte, :_nombre_tipo_transporte)")

    try:
        await db.execute(query, {
            "_cod_tipo_transporte": cod_tipo_transporte,
            "_nombre_tipo_transporte": tipo.nombre_tipo_transporte
        })
        await db.commit()
        return {"message": f"Tipo de transporte con ID {cod_tipo_transporte} modificado exitosamente"}
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=400, detail="No se pudo modificar el tipo de transporte.")
    
async def eliminar_tipo_transporte(db: AsyncSession, cod_tipo_transporte: int):
    # Verificar existencia
    result = await db.execute(
        select(TipoTransporte).where(TipoTransporte.cod_tipo_transporte == cod_tipo_transporte)
    )
    existente = result.scalar_one_or_none()
    if not existente:
        raise HTTPException(
            status_code=404,
            detail=f"No se encontró el tipo de transporte con ID {cod_tipo_transporte}"
        )

    query = text("CALL eliminar_tipo_transporte(:_cod_tipo_transporte)")

    try:
        await db.execute(query, {"_cod_tipo_transporte": cod_tipo_transporte})
        await db.commit()
        return {"message": f"Tipo de transporte con ID {cod_tipo_transporte} eliminado exitosamente"}
    except Exception as e:
        await db.rollback()
        error_str = str(e)

        if "en uso por" in error_str.lower():
            raise HTTPException(
                status_code=400,
                detail="Este tipo de transporte está en uso por uno o más vehículos y no se puede eliminar."
            )

        raise HTTPException(status_code=500, detail="Error interno al eliminar el tipo de transporte.")
    
def obtener_tipos_transporte(
    db: Session,skip: int = 0,limit: int = 10) -> List[TipoTransporte]:
    """
    Devuelve una lista de tipos de transporte paginada.
    - skip: cuántos registros omitir
    - limit: cuántos registros devolver como máximo
    """
    return (
        db.query(TipoTransporte).offset(skip).limit(limit).all()
    )

def obtener_tipo_transporte_por_id(
    db: Session,cod_tipo_transporte: int) -> TipoTransporte:
    """
    Devuelve un tipo de transporte por su ID.
    """
    tipo = (db.query(TipoTransporte).filter(TipoTransporte.cod_tipo_transporte == cod_tipo_transporte).first())

    if not tipo:
        raise HTTPException(
            status_code=404,
            detail=f"No se encontró el tipo de transporte con ID {cod_tipo_transporte}"
        )

    return tipo

async def insertar_vehiculo_motorista(db: AsyncSession, vehiculo: VehiculoMotoristaCreate):
    query = text("""
        CALL insertar_vehiculo_motorista(
            :_cod_persona,
            :_cod_tipo_transporte,
            :_modelo_transporte,
            :_numero_placa,
            :_chasis,
            :_cod_marca,
            :_estado
        )
    """)

    try:
        await db.execute(query, {
            "_cod_persona": vehiculo.cod_persona,
            "_cod_tipo_transporte": vehiculo.cod_tipo_transporte,
            "_modelo_transporte": vehiculo.modelo_transporte,
            "_numero_placa": vehiculo.numero_placa,
            "_chasis": vehiculo.chasis,
            "_cod_marca": vehiculo.cod_marca,
            "_estado": vehiculo.estado
        })
        await db.commit()
    except Exception as e:
        await db.rollback()
        raise

async def actualizar_vehiculo_motorista_crud(
    db: AsyncSession,
    cod_vehiculo: int,
    vehiculo: VehiculoMotoristaUpdate
):
    query = text("""
        CALL actualizar_vehiculo_motorista(
            :_cod_vehiculo,
            :_cod_tipo_transporte,
            :_modelo_transporte,
            :_numero_placa,
            :_chasis,
            :_cod_marca,
            :_estado
        )
    """)
    try:
        await db.execute(query, {
            "_cod_vehiculo": cod_vehiculo,
            "_cod_tipo_transporte": vehiculo.cod_tipo_transporte,
            "_modelo_transporte": vehiculo.modelo_transporte,
            "_numero_placa": vehiculo.numero_placa,
            "_chasis": vehiculo.chasis,
            "_cod_marca": vehiculo.cod_marca,
            "_estado": vehiculo.estado
        })
        await db.commit()
        return {"message": f"Vehículo con ID {cod_vehiculo} actualizado correctamente"}
    except Exception as e:
        await db.rollback()
        raise

async def eliminar_vehiculo_motorista(db: AsyncSession, cod_vehiculo: int):
    query = text("CALL eliminar_vehiculo_motorista(:_cod_vehiculo)")
    try:
        await db.execute(query, {"_cod_vehiculo": cod_vehiculo})
        await db.commit()
        return {"message": f"Vehículo con ID {cod_vehiculo} eliminado exitosamente"}
    except Exception as e:
        await db.rollback()
        raise

def obtener_vehiculos_motorista(db: Session,skip: int = 0,limit: int = 10) -> List[VehiculoMotorista]:
    return (db.query(VehiculoMotorista).offset(skip).limit(limit).all())

def obtener_vehiculo_motorista_por_id(db: Session, cod_vehiculo: int) -> VehiculoMotorista | None:
    return db.query(VehiculoMotorista).filter(VehiculoMotorista.cod_vehiculo == cod_vehiculo).first()

def obtener_vehiculos_por_estado(db: Session,estado: str,skip: int = 0,limit: int = 10) -> List[VehiculoMotorista]:
    return (db.query(VehiculoMotorista).filter(VehiculoMotorista.estado == estado).offset(skip).limit(limit).all())

def obtener_vehiculos_por_persona(db: Session,cod_persona: int,skip: int = 0,limit: int = 10) -> List[VehiculoMotorista]:
    return (db.query(VehiculoMotorista).filter(VehiculoMotorista.cod_persona == cod_persona).offset(skip).limit(limit).all())