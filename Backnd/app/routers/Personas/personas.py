from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ...crud.Personas.personas import insertar_persona, actualizar_persona, eliminar_persona, obtener_persona_por_id, obtener_todas_las_personas, insertar_tipo_persona, eliminar_tipo_persona
from ...schemas.Personas.personas import PersonaCreate, PersonaUpdate, Persona, TipoPersonaCreate, TipoPersona
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
        error_message = str(e.orig) if hasattr(e, 'orig') else str(e)
        raise HTTPException(status_code=400, detail=error_message)
    
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
        db_persona=eliminar_persona(db, cod_persona)
        if db_persona is None:
            raise HTTPException(status_code=404, detail="Empleado no encontrado")
        return {"message": "Empleado eliminado correctamente"}
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

# Ruta para insertar un nuevo tipo_persona
@router.post("/tipo_persona/")
def crear_tipo_persona(tipo_persona: TipoPersonaCreate, db: Session = Depends(get_db)):
    try:
        insertar_tipo_persona(db, tipo_persona)
        return {"message": "Tipo Persona insertada exitosamente"}
    except Exception as e: 
        error_message = str(e.orig) if hasattr(e, 'orig') else str(e)
        raise HTTPException(status_code=400, detail=error_message)  


# Ruta para eliminar un tipo_persona por ID
@router.delete("/tipo_persona/{cod_tipo_persona}")
def borrar_tipo_persona(cod_tipo_persona: int, db: Session = Depends(get_db)):
    try:
        db_tipo_persona = eliminar_tipo_persona(db, cod_tipo_persona)
        if db_tipo_persona is None:
            raise HTTPException(status_code=404, detail="Tipo Persona no encontrado")
        return {"message": "Tipo Persona eliminada exitosamente"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    

