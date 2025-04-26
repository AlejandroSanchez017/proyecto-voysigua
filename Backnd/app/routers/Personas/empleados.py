from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session, joinedload
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import select
from sqlalchemy import exists, and_
from app.database import get_async_db, get_sync_db  # ✅ Importamos ambas funciones correctamente
from sqlalchemy.exc import IntegrityError
from app.utils.utils import extraer_campo_foreign_key, extraer_campo_null
from app.models.Personas.empleados import Empleado as EmpleadoModel, VehiculoMotorista  # ✅ Corrección
from app.schemas.Personas.empleados import (
    EmpleadoCreate, EmpleadoResponse, NombreTipoEmpleadoCreate, TipoContrato,
    AreasCreate, TipoContratoCreate, EmpleadoDespedir, EmpleadoUpdate, NombreTipoEmpleado, Areas as AreasSchema, MarcaCreate,
    MarcaUpdate, MarcaResponse, TipoTransporteCreate, TipoTransporteUpdate, TipoTransporteResponse, VehiculoMotoristaCreate,
    VehiculoMotoristaUpdate, VehiculoMotoristaResponse
)
from app.crud.Personas.empleados import (
    insertar_empleado, actualizar_empleado_crud, despedir_empleado_crud, eliminar_empleado, insertar_tipo_empleado, 
    obtener_tipos_empleado, eliminar_tipo_empleado, insertar_area, obtener_areas, eliminar_area, insertar_tipo_contrato, obtener_tipos_contrato,
    eliminar_tipo_contrato, insertar_marca, modificar_marca, eliminar_marca, obtener_marcas, obtener_marca_por_id,
    insertar_tipo_transporte, modificar_tipo_transporte, eliminar_tipo_transporte, obtener_tipos_transporte, 
    obtener_tipo_transporte_por_id, insertar_vehiculo_motorista, actualizar_vehiculo_motorista_crud, 
    eliminar_vehiculo_motorista, obtener_vehiculos_motorista, obtener_vehiculo_motorista_por_id, obtener_vehiculos_por_estado,
    obtener_vehiculos_por_persona
)
from typing import List
import logging

logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)

router = APIRouter()

@router.post("/empleados/", response_model=dict)
async def crear_empleado(empleado: EmpleadoCreate, db: AsyncSession = Depends(get_async_db)):
    try:
        await insertar_empleado(db, empleado)
        return {"message": "Empleado insertado correctamente"}

    except IntegrityError as e:
        error_msg = str(e.orig) if hasattr(e, "orig") else str(e)
        logger.error(f"Error de integridad al insertar empleado: {error_msg}")

        # Clave foránea inválida
        if "foreign key" in error_msg.lower() or "llave foránea" in error_msg.lower():
            campo = extraer_campo_foreign_key(error_msg)
            raise HTTPException(
                status_code=400,
                detail=f"El valor ingresado para '{campo}' no existe en la base de datos. Verifica que el dato sea válido."
            )

        # Clave única duplicada (si tuvieras alguna en empleados)
        if "duplicate key" in error_msg.lower():
            raise HTTPException(
                status_code=400,
                detail="Ya existe un empleado con un valor que debe ser único. Verifica los datos ingresados."
            )

        # Campo obligatorio omitido
        if "null value in column" in error_msg.lower():
            campo = extraer_campo_null(error_msg)
            raise HTTPException(
                status_code=400,
                detail=f"El campo '{campo}' es obligatorio y no puede estar vacío."
            )

        raise HTTPException(status_code=400, detail="Error de integridad en la base de datos.")

    except Exception as e:
        logger.error(f"Error general al crear empleado: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))


@router.put("/empleados/{cod_empleado}", response_model=dict)
async def modificar_empleado(
    cod_empleado: int,
    empleado: EmpleadoUpdate,
    db: AsyncSession = Depends(get_async_db)
):
    try:
        await actualizar_empleado_crud(db, cod_empleado, empleado)
        return {"message": "Empleado actualizado correctamente"}

    except IntegrityError as e:
        error_msg = str(e.orig) if hasattr(e, "orig") else str(e)
        logger.error(f"Error de integridad en actualización: {type(e.orig)} - {error_msg}")

        # 🔍 Clave foránea inválida
        if "foreign key" in error_msg.lower() or "llave foránea" in error_msg.lower():
            campo = extraer_campo_foreign_key(error_msg)
            raise HTTPException(
                status_code=400,
                detail=f"El valor ingresado para '{campo}' no existe en la base de datos. Verifica que sea válido."
            )

        # ❗ Clave única duplicada (si aplica)
        if "duplicate key" in error_msg.lower():
            raise HTTPException(
                status_code=400,
                detail="Ya existe un empleado con un valor que debe ser único. Verifica los datos ingresados."
            )

        # ⚠️ Campo obligatorio omitido
        if "null value in column" in error_msg.lower():
            campo = extraer_campo_null(error_msg)
            raise HTTPException(
                status_code=400,
                detail=f"El campo '{campo}' es obligatorio y no puede estar vacío."
            )

        raise HTTPException(status_code=400, detail="Error de integridad en la base de datos.")

    except Exception as e:
        error_str = str(e)
        logger.error(f"Error general al actualizar empleado: {error_str}")

        # 💡 Caso: procedimiento lanza error personalizado
        if "No se encontró el empleado con ID" in error_str:
            raise HTTPException(
                status_code=404,
                detail=f"No se encontró el empleado con ID {cod_empleado}"
            )

        raise HTTPException(status_code=400, detail=error_str)

@router.put("/empleados/despedir/{cod_empleado}")
async def despedir_empleado(
    cod_empleado: int,
    datos: EmpleadoDespedir,
    db: AsyncSession = Depends(get_async_db)
):
    try:
        result = await despedir_empleado_crud(db, cod_empleado, datos)
        return result
    except Exception as e:
        # Conviertes la excepción a string
        error_message = str(e)

        # Si el procedure lanza "No existe el empleado..." o "No se pudo despedir..."
        # lo detectas en la cadena y devuelves solo esa parte
        if "No existe el empleado con el código" in error_message:
            error_message = f"No existe el empleado con el código {cod_empleado}"
        elif "No se pudo despedir al empleado con código" in error_message:
            error_message = f"No se pudo despedir al empleado con código {cod_empleado}, puede que no exista o ya esté inactivo"

        raise HTTPException(status_code=400, detail=error_message)

@router.delete("/empleados/{cod_empleado}")
async def borrar_empleado(cod_empleado: int, db: AsyncSession = Depends(get_async_db)):
    try:
        db_empleado = await eliminar_empleado(db, cod_empleado)
        if db_empleado is None:
            raise HTTPException(status_code=404, detail="Empleado no encontrado")
        return {"message": "Empleado eliminado correctamente"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/empleados/", response_model=List[EmpleadoResponse])
def obtener_todos_los_empleados(db: Session = Depends(get_sync_db)):
    empleados = db.execute(
        select(EmpleadoModel)
        .options(
            joinedload(EmpleadoModel.tipo_empleado),
            joinedload(EmpleadoModel.area),
            joinedload(EmpleadoModel.contrato)
        )
    ).scalars().all()

    if not empleados:
        raise HTTPException(status_code=404, detail="No hay empleados registrados")

    # ✅ Convertimos a Pydantic incluyendo claves foráneas
    return [
        EmpleadoResponse(
            cod_empleado=empleado.cod_empleado,
            cod_persona=empleado.cod_persona,
            cod_tipo_empleado=empleado.cod_tipo_empleado,  # ✅ Agregamos el código
            cod_area=empleado.cod_area,  # ✅ Agregamos el código
            cod_tipo_contrato=empleado.cod_tipo_contrato,  # ✅ Agregamos el código
            fecha_salida=empleado.fecha_salida,
            motivo_salida=empleado.motivo_salida,
            fecha_contratacion=empleado.fecha_contratacion,
            salario=empleado.salario,
            estado_empleado=empleado.estado_empleado,
        )
        for empleado in empleados
    ]

# ✅ Endpoint para obtener un empleado por ID
@router.get("/empleados/{cod_empleado}", response_model=EmpleadoResponse)
def obtener_empleado_por_id_endpoint(cod_empleado: int, db: Session = Depends(get_sync_db)):
    empleado = db.execute(
        select(EmpleadoModel)
        .options(
            joinedload(EmpleadoModel.tipo_empleado),
            joinedload(EmpleadoModel.area),
            joinedload(EmpleadoModel.contrato)
        )
        .filter(EmpleadoModel.cod_empleado == cod_empleado)
    ).scalars().first()

    if not empleado:
        raise HTTPException(status_code=404, detail="Empleado no encontrado")

    # ✅ Convertimos la relación en un formato adecuado para la API
    return EmpleadoResponse(
        cod_empleado=empleado.cod_empleado,
        cod_persona=empleado.cod_persona,
        cod_tipo_empleado=empleado.cod_tipo_empleado,
        cod_area=empleado.cod_area,
        cod_tipo_contrato=empleado.cod_tipo_contrato,
        fecha_salida=empleado.fecha_salida,
        motivo_salida=empleado.motivo_salida,
        fecha_contratacion=empleado.fecha_contratacion,
        salario=empleado.salario,
        estado_empleado=empleado.estado_empleado,
    )

@router.post("/tipo_empleado/")
async def crear_tipo_empleado(nombre_tipo_empleado: NombreTipoEmpleadoCreate, db: AsyncSession = Depends(get_async_db)):
    try:
        await insertar_tipo_empleado(db, nombre_tipo_empleado)
        return {"message": "Tipo empleado insertado correctamente"}
    except Exception as e:
        error_message = str(e.orig) if hasattr(e, 'orig') else str(e)
        raise HTTPException(status_code=400, detail=error_message)

@router.get("/tipo_empleado/", response_model=List[NombreTipoEmpleado])
async def get_tipos_empleado(db: AsyncSession = Depends(get_async_db)):
    """
    Obtiene todos los registros de tipo_empleado.
    """
    try:
        tipos = await obtener_tipos_empleado(db)
        return tipos  # Si está vacío, retorna simplemente []
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/tipo_empleado/{cod_tipo_empleado}")
async def borrar_tipo_empleado(cod_tipo_empleado: int, db: AsyncSession = Depends(get_async_db)):
    try:
        db_nombre_tipo_empleado = await eliminar_tipo_empleado(db, cod_tipo_empleado)
        if db_nombre_tipo_empleado is None:
            raise HTTPException(status_code=404, detail="Tipo empleado no encontrado")
        return {"message": "Tipo empleado eliminado exitosamente"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/areas/")
async def crear_area(nombre_area: AreasCreate, db: AsyncSession = Depends(get_async_db)):
    try:
        await insertar_area(db, nombre_area)
        return {"message": "Área insertada correctamente"}
    except Exception as e:
        error_message = str(e.orig) if hasattr(e, 'orig') else str(e)
        raise HTTPException(status_code=400, detail=error_message)

@router.get("/areas/", response_model=List[AreasSchema])
async def get_areas(db: AsyncSession = Depends(get_async_db)):
    try:
        lista_areas = await obtener_areas(db)
        if not lista_areas:
            # Manejo de "no hay áreas"
            return []
        return lista_areas  # Retornamos la lista tal cual, FastAPI hará el parseo a AreasSchema
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/areas/{cod_area}")
async def borrar_area(cod_area: int, db: AsyncSession = Depends(get_async_db)):
    try:
        db_areas = await eliminar_area(db, cod_area)
        if db_areas is None:
            raise HTTPException(status_code=404, detail="Área no encontrada")
        return {"message": "Área eliminada exitosamente"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/tipo_contrato/")
async def crear_tipo_contrato(tipo_contrato: TipoContratoCreate, db: AsyncSession = Depends(get_async_db)):
    try:
        await insertar_tipo_contrato(db, tipo_contrato)
        return {"message": "Tipo de contrato insertado correctamente"}
    except Exception as e:
        error_message = str(e.orig) if hasattr(e, 'orig') else str(e)
        raise HTTPException(status_code=400, detail=error_message)

@router.get("/tipo_contrato/", response_model=List[TipoContrato])
async def get_tipos_contrato(db: AsyncSession = Depends(get_async_db)):
    """
    Devuelve todos los tipos de contrato registrados en la base de datos.
    """
    try:
        lista_contratos = await obtener_tipos_contrato(db)
        return lista_contratos
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/tipo_contrato/{cod_tipo_contrato}")
async def borrar_tipo_contrato(cod_tipo_contrato: int, db: AsyncSession = Depends(get_async_db)):
    try:
        db_tipo_contrato = await eliminar_tipo_contrato(db, cod_tipo_contrato)
        if db_tipo_contrato is None:
            raise HTTPException(status_code=404, detail="Tipo de contrato no encontrado")
        return {"message": "Tipo de contrato eliminado exitosamente"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@router.post("/marcas/", response_model=dict)
async def crear_marca(
    marca: MarcaCreate,
    db: AsyncSession = Depends(get_async_db)
):
    try:
        return await insertar_marca(db, marca)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error al insertar la marca.")

@router.put("/marcas/{cod_marca}", response_model=dict)
async def actualizar_marca(
    cod_marca: int,
    marca: MarcaUpdate,
    db: AsyncSession = Depends(get_async_db)
):
    try:
        return await modificar_marca(db, cod_marca, marca)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error al modificar la marca.")
    
@router.delete("/marcas/{cod_marca}", response_model=dict)
async def eliminar_marca_api(
    cod_marca: int,
    db: AsyncSession = Depends(get_async_db)
):
    try:
        return await eliminar_marca(db, cod_marca)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail="No se pudo eliminar la marca.")
    
@router.get("/marcas", response_model=List[MarcaResponse])
def listar_marcas(
    skip: int = Query(0, ge=0, description="Registros a omitir"),
    limit: int = Query(10, gt=0, description="Cantidad máxima de registros a devolver"),
    db: Session = Depends(get_sync_db)
):
    return obtener_marcas(db, skip=skip, limit=limit)

@router.get("/marca/{cod_marca}", response_model=MarcaResponse)
def obtener_marca(
    cod_marca: int,
    db: Session = Depends(get_sync_db)
):
    return obtener_marca_por_id(db, cod_marca)

@router.post("/tipos_transporte/", response_model=dict)
async def crear_tipo_transporte(
    tipo: TipoTransporteCreate,
    db: AsyncSession = Depends(get_async_db)
):
    try:
        return await insertar_tipo_transporte(db, tipo)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error al insertar el tipo de transporte.")
    
@router.put("/tipos_transporte/{cod_tipo_transporte}", response_model=dict)
async def actualizar_tipo_transporte(
    cod_tipo_transporte: int,
    tipo: TipoTransporteUpdate,
    db: AsyncSession = Depends(get_async_db)
):
    try:
        return await modificar_tipo_transporte(db, cod_tipo_transporte, tipo)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error al modificar el tipo de transporte.")
    
@router.delete("/tipos_transporte/{cod_tipo_transporte}", response_model=dict)
async def eliminar_tipo_transporte_api(
    cod_tipo_transporte: int,
    db: AsyncSession = Depends(get_async_db)
):
    try:
        return await eliminar_tipo_transporte(db, cod_tipo_transporte)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail="No se pudo eliminar el tipo de transporte.")
    
@router.get("/tipos_transporte", response_model=List[TipoTransporteResponse])
def listar_tipos_transporte(
    skip: int = Query(0, ge=0, description="Registros a omitir"),
    limit: int = Query(10, gt=0, description="Cantidad máxima de registros a devolver"),
    db: Session = Depends(get_sync_db)
):
    return obtener_tipos_transporte(db, skip=skip, limit=limit)

@router.get("/tipos_transporte/{cod_tipo_transporte}", response_model=TipoTransporteResponse)
def obtener_tipo_transporte(
    cod_tipo_transporte: int,
    db: Session = Depends(get_sync_db)
):
    return obtener_tipo_transporte_por_id(db, cod_tipo_transporte)


@router.post("/vehiculo_motorista/", response_model=dict)
async def crear_vehiculo_motorista(
    vehiculo: VehiculoMotoristaCreate,
    db: AsyncSession = Depends(get_async_db)
):
    try:
        await insertar_vehiculo_motorista(db, vehiculo)
        return {"message": "Vehículo del motorista insertado exitosamente"}

    except IntegrityError as e:
        error_msg = str(e.orig) if hasattr(e, "orig") else str(e)
        logger.error(f"Error de integridad al insertar vehículo: {type(e.orig)} - {error_msg}")

        # 🔍 Clave foránea inválida
        if "foreign key" in error_msg.lower() or "llave foránea" in error_msg.lower():
            campo = extraer_campo_foreign_key(error_msg)
            raise HTTPException(
                status_code=400,
                detail=f"El valor ingresado para '{campo}' no existe en la base de datos. Verifica que sea válido."
            )

        # ❗ Placa duplicada
        if (
            "duplicate key" in error_msg.lower() and "numero_placa" in error_msg.lower()
        ) or "tbl_vehiculos_motorista_numero_placa_key" in error_msg.lower():
            raise HTTPException(
                status_code=400,
                detail="El número de placa ingresado ya está registrado. Debe ser único."
            )

        # ❗ Chasis duplicado
        if (
            "duplicate key" in error_msg.lower() and "chasis" in error_msg.lower()
        ) or "tbl_vehiculos_motorista_chasis_key" in error_msg.lower() or "unique_chasis" in error_msg.lower():
            raise HTTPException(
                status_code=400,
                detail="El número de chasis ingresado ya está registrado. Debe ser único."
            )

        # ⚠️ Campo obligatorio omitido
        if "null value in column" in error_msg.lower():
            campo = extraer_campo_null(error_msg)
            raise HTTPException(
                status_code=400,
                detail=f"El campo '{campo}' es obligatorio y no puede estar vacío."
            )

        raise HTTPException(status_code=400, detail="Error de integridad en la base de datos.")

    except Exception as e:
        logger.error(f"Error general al insertar vehículo: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
    
@router.put("/vehiculo_motorista/{cod_vehiculo}", response_model=dict)
async def modificar_vehiculo_motorista(
    cod_vehiculo: int,
    vehiculo: VehiculoMotoristaUpdate,
    db: AsyncSession = Depends(get_async_db)
):
    # Validar existencia del vehículo
    result = await db.execute(
        select(VehiculoMotorista).where(VehiculoMotorista.cod_vehiculo == cod_vehiculo)
    )
    existe = result.scalar_one_or_none()
    if not existe:
        raise HTTPException(status_code=404, detail=f"No se encontró el vehículo con ID {cod_vehiculo}")

    # Validar número de placa duplicado
    placa_duplicada = await db.execute(
        select(exists().where(
            and_(
                VehiculoMotorista.numero_placa == vehiculo.numero_placa,
                VehiculoMotorista.cod_vehiculo != cod_vehiculo
            )
        ))
    )
    if placa_duplicada.scalar():
        raise HTTPException(
            status_code=400,
            detail="El número de placa ingresado ya está registrado. Debe ser único."
        )

    # Validar número de chasis duplicado
    chasis_duplicado = await db.execute(
        select(exists().where(
            and_(
                VehiculoMotorista.chasis == vehiculo.chasis,
                VehiculoMotorista.cod_vehiculo != cod_vehiculo
            )
        ))
    )
    if chasis_duplicado.scalar():
        raise HTTPException(
            status_code=400,
            detail="El número de chasis ingresado ya está registrado. Debe ser único."
        )

    # Ejecutar procedimiento
    try:
        return await actualizar_vehiculo_motorista_crud(db, cod_vehiculo, vehiculo)
    except Exception as e:
        logger.error(f"Error general al actualizar vehículo: {str(e)}")
        raise HTTPException(status_code=400, detail="Error al actualizar el vehículo.")
    
@router.delete("/vehiculo_motorista/{cod_vehiculo}", response_model=dict)
async def eliminar_vehiculo_motorista_api(
    cod_vehiculo: int,
    db: AsyncSession = Depends(get_async_db)
):
    # Verificar si el vehículo existe
    result = await db.execute(
        select(VehiculoMotorista).where(VehiculoMotorista.cod_vehiculo == cod_vehiculo)
    )
    existe = result.scalar_one_or_none()
    if not existe:
        raise HTTPException(status_code=404, detail=f"No se encontró el vehículo con ID {cod_vehiculo}")

    # Eliminar
    try:
        return await eliminar_vehiculo_motorista(db, cod_vehiculo)
    except Exception as e:
        logger.error(f"Error al eliminar vehículo: {str(e)}")
        raise HTTPException(status_code=400, detail="No se pudo eliminar el vehículo.")
    
@router.get("/vehiculo_motorista", response_model=List[VehiculoMotoristaResponse])
def listar_vehiculos_motorista(
    skip: int = Query(0, ge=0, description="Registros a omitir"),
    limit: int = Query(10, gt=0, le=100, description="Máximo de registros a retornar"),
    db: Session = Depends(get_sync_db)
):
    vehiculos = obtener_vehiculos_motorista(db, skip=skip, limit=limit)
    if not vehiculos:
        raise HTTPException(status_code=404, detail="No se encontraron vehículos registrados")
    return vehiculos

@router.get("/vehiculo_motorista/{cod_vehiculo}", response_model=VehiculoMotoristaResponse)
def obtener_vehiculo_motorista(
    cod_vehiculo: int,
    db: Session = Depends(get_sync_db)
):
    vehiculo = obtener_vehiculo_motorista_por_id(db, cod_vehiculo)
    if not vehiculo:
        raise HTTPException(status_code=404, detail=f"No se encontró el vehículo con ID {cod_vehiculo}")
    return vehiculo

@router.get("/vehiculo_motorista/estado/{estado}", response_model=List[VehiculoMotoristaResponse])
def listar_vehiculos_por_estado(
    estado: str,
    skip: int = Query(0, ge=0, description="Registros a omitir"),
    limit: int = Query(10, gt=0, le=100, description="Máximo de registros a retornar"),
    db: Session = Depends(get_sync_db)
):
    estado = estado.upper()
    if estado not in ("A", "I"):
        raise HTTPException(status_code=400, detail="El estado debe ser 'A' (activo) o 'I' (inactivo)")

    vehiculos = obtener_vehiculos_por_estado(db, estado, skip, limit)
    if not vehiculos:
        raise HTTPException(status_code=404, detail=f"No se encontraron vehículos con estado '{estado}'")
    return vehiculos

@router.get("/vehiculo_motorista/persona/{cod_persona}", response_model=List[VehiculoMotoristaResponse])
def listar_vehiculos_por_persona(
    cod_persona: int,
    skip: int = Query(0, ge=0, description="Registros a omitir"),
    limit: int = Query(10, gt=0, le=100, description="Máximo de registros a retornar"),
    db: Session = Depends(get_sync_db)
):
    vehiculos = obtener_vehiculos_por_persona(db, cod_persona, skip, limit)
    if not vehiculos:
        raise HTTPException(status_code=404, detail=f"No se encontraron vehículos registrados para la persona con ID {cod_persona}")
    return vehiculos