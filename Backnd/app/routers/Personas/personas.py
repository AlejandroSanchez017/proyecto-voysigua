from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ...crud.Personas.personas import insertar_persona, actualizar_persona, eliminar_persona, obtener_persona_por_id, obtener_todas_las_personas
from ...schemas.Personas.personas import PersonaCreate, PersonaUpdate, Persona
from ...database import get_db

router = APIRouter()

# Endpoint para consultar una persona por ID

# Endpint para consultar toda la tabla de personas

# Endpoint para insertar una nueva persona
@router.post("/personas/")
def crear_persona(persona: PersonaCreate, db: Session = Depends(get_db)):
    try:
        insertar_persona(db, persona)
        return {"message": "Persona insertada exitosamente"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# Endpoint para actualizar una persona existente
@router.put("/personas/{cod_persona}")
def modificar_persona(cod_persona: int, persona: PersonaUpdate, db: Session = Depends(get_db)):
    try:
        actualizar_persona(db, cod_persona, persona)
        return {"message": "Persona actualizada exitosamente"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# Endpoint para eliminar una persona
@router.delete("/personas/{cod_persona}")
def borrar_persona(cod_persona: int, db: Session = Depends(get_db)):
    try:
        eliminar_persona(db, cod_persona)
        return {"message": "Persona eliminada exitosamente"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
    # Ruta para obtener una persona por ID
@router.get("/personas/{persona_id}", response_model=Persona)
def leer_persona(persona_id: int, db: Session = Depends(get_db)):
    persona = obtener_persona_por_id(db, persona_id)
    if not persona:
        raise HTTPException(status_code=404, detail="Persona no encontrada")
    return persona

# Ruta para obtener todas las personas
@router.get("/personas/", response_model=list[Persona])
def leer_todas_las_personas(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    personas = obtener_todas_las_personas(db, skip=skip, limit=limit)
    return personas
