
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
    async with db.begin():
        await db.execute(query, {"cod_persona": cod_persona, **persona.model_dump(exclude_unset=True)})
        await db.commit()

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
    async with db.begin():
        db.add(db_tipo_persona)
        await db.commit()
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
