from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session
from sqlalchemy.sql import select
from app.database import get_async_db, get_sync_db
from sqlalchemy.exc import IntegrityError
from app.utils.utils import extraer_campo_foreign_key, extraer_campo_null
from app.crud.Personas.personas import (
    insertar_persona, actualizar_persona, eliminar_persona,
    obtener_persona_por_id, insertar_tipo_persona, eliminar_tipo_persona
)
from app.models.Personas.personas import Persona as PersonaModel, TipoPersona as TipoPersonaModel
from app.schemas.Personas.personas import PersonaCreate, PersonaUpdate, PersonaResponse, TipoPersonaCreate, TipoPersona
from typing import List
import logging

logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)
router = APIRouter()

# ✅ Endpoint para insertar una nueva persona (ASÍNCRONO)
@router.post("/personas/", response_model=dict)
async def crear_persona(persona: PersonaCreate, db: AsyncSession = Depends(get_async_db)):
    try:
        await insertar_persona(db, persona)
        return {"message": "Persona insertada exitosamente"}

    except IntegrityError as e:
        error_msg = str(e.orig) if hasattr(e, "orig") else str(e)
        logger.error(f"Error de integridad al insertar persona: {error_msg}")

        # 🟠 Clave foránea: cod_tipo_persona no existe
        if "foreign key" in error_msg.lower() or "llave foránea" in error_msg.lower():
            campo = extraer_campo_foreign_key(error_msg)
            if campo == "cod_tipo_persona":
                raise HTTPException(
                    status_code=400,
                    detail="El tipo de persona ingresado no existe. Verifica que 'cod_tipo_persona' sea válido."
                )
            raise HTTPException(
                status_code=400,
                detail=f"El valor ingresado para '{campo}' no existe en la base de datos."
            )

        # 🟠 Clave única duplicada: número de identificación ya registrado
        if (
            "dni" in error_msg.lower() and
            ("tbl_personas_dni_key" in error_msg.lower() or "restricción de unicidad" in error_msg.lower())
        ):
            raise HTTPException(
                status_code=400,
                detail="Ya existe una persona registrada con este número de identificación."
            )

        # 🟠 Campo obligatorio omitido
        if "null value in column" in error_msg.lower():
            campo = extraer_campo_null(error_msg)
            raise HTTPException(
                status_code=400,
                detail=f"El campo '{campo}' es obligatorio y no puede estar vacío."
            )

        raise HTTPException(status_code=400, detail="Error de integridad en la base de datos.")

    except Exception as e:
        logger.error(f"Error general al insertar persona: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))

# ✅ Endpoint para actualizar una persona (ASÍNCRONO)
@router.put("/personas/{cod_persona}", response_model=dict)
async def modificar_persona(
    cod_persona: int,
    persona: PersonaUpdate,
    db: AsyncSession = Depends(get_async_db)
):
    try:
        await actualizar_persona(db, cod_persona, persona)
        return {"message": "Persona actualizada exitosamente"}

    except IntegrityError as e:
        error_msg = str(e.orig) if hasattr(e, "orig") else str(e)
        logger.error(f"Error de integridad al actualizar persona: {error_msg}")

        # 🟠 Clave foránea: cod_tipo_persona no existe
        if "foreign key" in error_msg.lower() or "llave foránea" in error_msg.lower():
            campo = extraer_campo_foreign_key(error_msg)
            if campo == "cod_tipo_persona":
                raise HTTPException(
                    status_code=400,
                    detail="El tipo de persona ingresado no existe. Verifica que 'cod_tipo_persona' sea válido."
                )
            raise HTTPException(
                status_code=400,
                detail=f"El valor ingresado para '{campo}' no existe en la base de datos."
            )

        # 🟠 Clave única duplicada: número de identificación ya registrado
        if (
            "dni" in error_msg.lower() and
            ("tbl_personas_dni_key" in error_msg.lower() or "restricción de unicidad" in error_msg.lower())
        ):
            raise HTTPException(
                status_code=400,
                detail="Ya existe otra persona registrada con este número de identificación."
            )

        # 🟠 Campo obligatorio omitido
        if "null value in column" in error_msg.lower():
            campo = extraer_campo_null(error_msg)
            raise HTTPException(
                status_code=400,
                detail=f"El campo '{campo}' es obligatorio y no puede estar vacío."
            )

        raise HTTPException(status_code=400, detail="Error de integridad en la base de datos.")

    except Exception as e:
        logger.error(f"Error general al actualizar persona {cod_persona}: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))

# ✅ Endpoint para eliminar una persona (ASÍNCRONO)
@router.delete("/personas/{cod_persona}", response_model=dict)
async def borrar_persona(cod_persona: int, db: AsyncSession = Depends(get_async_db)):
    db_persona = await eliminar_persona(db, cod_persona)
    if db_persona is None:
        raise HTTPException(status_code=404, detail="Persona no encontrada")
    return {"message": "Persona eliminada correctamente"}

# ✅ Endpoint para obtener una persona por ID (ASÍNCRONO)
@router.get("/personas/{persona_id}", response_model=PersonaResponse)
async def leer_persona(persona_id: int, db: AsyncSession = Depends(get_async_db)):
    persona = await obtener_persona_por_id(db, persona_id)
    if not persona:
        raise HTTPException(status_code=404, detail="Persona no encontrada")
    return PersonaResponse.model_validate(persona)

# ✅ Ruta para obtener todas las personas (SÍNCRONA)
@router.get("/personas", response_model=List[PersonaResponse])
def obtener_todas_las_personas(skip: int = 0, limit: int = 10, db: Session = Depends(get_sync_db)):  
    result = db.execute(select(PersonaModel).offset(skip).limit(limit))  # ✅ No usar await aquí
    return result.scalars().all()

# ✅ Ruta para insertar un nuevo tipo_persona (ASÍNCRONO)
@router.post("/tipo_persona/", response_model=dict)
async def crear_tipo_persona(tipo_persona: TipoPersonaCreate, db: AsyncSession = Depends(get_async_db)):
    try:
        await insertar_tipo_persona(db, tipo_persona)
        return {"message": "Tipo Persona insertada exitosamente"}
    except Exception as e:
        error_message = str(e.orig) if hasattr(e, 'orig') else str(e)
        logger.error(f"Error al insertar TipoPersona: {error_message}")
        raise HTTPException(status_code=400, detail=error_message)

# ✅ Ruta para eliminar un tipo_persona (ASÍNCRONO)
@router.delete("/tipo_persona/{cod_tipo_persona}", response_model=dict)
async def borrar_tipo_persona(cod_tipo_persona: int, db: AsyncSession = Depends(get_async_db)):
    db_tipo_persona = await eliminar_tipo_persona(db, cod_tipo_persona)
    if db_tipo_persona is None:
        raise HTTPException(status_code=404, detail="Tipo Persona no encontrada")
    return {"message": "Tipo Persona eliminada exitosamente"}

# ✅ Obtener todos los tipos de persona (SÍNCRONO)
@router.get("/tipo_persona/", response_model=List[TipoPersona])
def obtener_todos_los_tipos_persona(db: Session = Depends(get_sync_db)):
    # ✅ Ahora seleccionamos el modelo correcto
    tipos_persona = db.execute(select(TipoPersonaModel)).scalars().all()  

    if not tipos_persona:
        raise HTTPException(status_code=404, detail="No hay tipos de persona registrados")

    # ✅ Convertimos los resultados de SQLAlchemy a Pydantic
    return [TipoPersona.model_validate(tp) for tp in tipos_persona]