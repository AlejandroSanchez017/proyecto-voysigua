from sqlalchemy.orm import Session
from sqlalchemy.sql import text
from ...schemas.Personas.personas import PersonaCreate, PersonaUpdate
from ...models.Personas.personas import Persona

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