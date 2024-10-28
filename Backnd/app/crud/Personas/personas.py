from sqlalchemy.orm import Session
from sqlalchemy.sql import text
from ...schemas.Personas.personas import PersonaCreate, PersonaUpdate, TipoPersonaCreate
from ...models.Personas.personas import Persona, TipoPersona

# Insertar persona
def insertar_persona(db: Session, persona: PersonaCreate):
    query = text("""
        CALL insertar_persona(:cod_tipo_persona, :dni, :primer_nombre, :apellido, 
                              :fecha_nacimiento, :sexo, :correo, :estado)
    """)
    db.execute(query, {
        "cod_tipo_persona": persona.cod_tipo_persona,
        "dni": persona.DNI,
        "primer_nombre": persona.primer_nombre,
        "apellido": persona.apellido,
        "fecha_nacimiento": persona.fecha_nacimiento,
        "sexo": persona.sexo,
        "correo": persona.correo,
        "estado": persona.estado
    })
    db.commit()

# Actualizar persona
def actualizar_persona(db: Session, cod_persona: int, persona: PersonaUpdate):
    query = text("""
        CALL actualizar_persona(:cod_persona, :cod_tipo_persona, :primer_nombre, :apellido,
                                :fecha_nacimiento, :sexo, :correo, :estado)
    """)
    db.execute(query, {
        "cod_persona": cod_persona,
        "cod_tipo_persona": persona.cod_tipo_persona,
        "primer_nombre": persona.primer_nombre,
        "apellido": persona.apellido,
        "fecha_nacimiento": persona.fecha_nacimiento,
        "sexo": persona.sexo,
        "correo": persona.correo,
        "estado": persona.estado
    })
    db.commit()

# Eliminar persona
def eliminar_persona(db: Session, cod_persona: int):
    query = text("CALL eliminar_persona(:cod_persona)")
    db.execute(query, {"cod_persona": cod_persona})
    db.commit()

# Obtener persona por ID
def obtener_persona_por_id(db: Session, persona_id: int):
    return db.query(Persona).filter(Persona.cod_persona == persona_id).first()

# Obtener todas las personas
def obtener_todas_las_personas(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Persona).offset(skip).limit(limit).all()

# Insertar TipoPersona
def insertar_tipo_persona(db: Session, tipo_persona: TipoPersonaCreate):
    db_tipo_persona = TipoPersona(tipo_persona=tipo_persona.tipo_persona)
    db.add(db_tipo_persona)
    db.commit()
    db.refresh(db_tipo_persona)  # Actualiza el objeto con los datos más recientes de la DB
    return db_tipo_persona

# Eliminar TipoPersona
def eliminar_tipo_persona(db: Session, cod_tipo_persona: int):
    db_tipo_persona = db.query(TipoPersona).filter(TipoPersona.cod_tipo_persona == cod_tipo_persona).first()
    if db_tipo_persona:
        db.delete(db_tipo_persona)
        db.commit()
        return db_tipo_persona
    return None