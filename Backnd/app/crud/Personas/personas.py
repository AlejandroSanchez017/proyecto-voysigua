from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import text, select
from app.schemas.Personas.personas import PersonaCreate, PersonaUpdate, TipoPersonaCreate
from app.models.Personas.personas import Persona, TipoPersona

# Insertar persona usando procedimiento almacenado
async def insertar_persona(db: AsyncSession, persona: PersonaCreate):
    query = text("""
        CALL insertar_persona(:cod_tipo_persona, :dni, :primer_nombre, :apellido, 
                              :fecha_nacimiento, :sexo, :correo, :estado)
    """)
    async with db.begin():
        await db.execute(query, persona.model_dump())
        await db.commit()

# Actualizar persona
async def actualizar_persona(db: AsyncSession, cod_persona: int, persona: PersonaUpdate):
    # Verificar si existe
    check_query = text("SELECT 1 FROM tbl_personas WHERE cod_persona = :id")
    result = await db.execute(check_query, {"id": cod_persona})
    if not result.scalar():
        raise HTTPException(status_code=404, detail=f"No se encontró la persona con ID {cod_persona}")

    query = text("""
        CALL actualizar_persona(
            :cod_persona,
            :cod_tipo_persona,
            :primer_nombre,
            :apellido,
            :fecha_nacimiento,
            :sexo,
            :correo,
            :estado
        )
    """)

    try:
        # Sin 'async with db.begin()'
        await db.execute(
            query,
            {"cod_persona": cod_persona, **persona.model_dump(exclude_unset=True)}
        )
        await db.commit()  # commit manual
        return {"message": "Persona actualizada exitosamente"}
    except Exception as e:
        await db.rollback()  # rollback manual si hay error
        raise HTTPException(status_code=400, detail=str(e))

# Eliminar persona
async def eliminar_persona(db: AsyncSession, cod_persona: int):
    async with db.begin():
        db_persona = await db.get(Persona, cod_persona)
        if not db_persona:
            return None
        await db.delete(db_persona)
        await db.commit()
        return db_persona

# Obtener persona por ID
async def obtener_persona_por_id(db: AsyncSession, persona_id: int):
    persona = await db.get(Persona, persona_id)
    return persona if persona else None

# Obtener todas las personas
async def obtener_todas_las_personas(db: AsyncSession, skip: int = 0, limit: int = 10):
    result = await db.execute(select(Persona).offset(skip).limit(limit))
    return result.scalars().all()

# Insertar TipoPersona
async def insertar_tipo_persona(db: AsyncSession, tipo_persona: TipoPersonaCreate):
    db_tipo_persona = TipoPersona(tipo_persona=tipo_persona.tipo_persona)
    db.add(db_tipo_persona)
    await db.commit()  # ✅ Hacemos commit aquí sin usar `async with db.begin()`
    await db.refresh(db_tipo_persona)
    return db_tipo_persona

# Eliminar TipoPersona
async def eliminar_tipo_persona(db: AsyncSession, cod_tipo_persona: int):
    async with db.begin():
        db_tipo_persona = await db.get(TipoPersona, cod_tipo_persona)
        if not db_tipo_persona:
            return None
        await db.delete(db_tipo_persona)
        await db.commit()
        return db_tipo_persona
    
# Obtener todos los tipos de persona
async def obtener_tipos_persona(db: AsyncSession):
    result = await db.execute(select(TipoPersona))
    return result.scalars().all()
