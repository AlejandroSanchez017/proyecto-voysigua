from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ...crud.Seguridad.Usuarios import insertar_usuario, actualizar_usuario, eliminar_usuario, obtener_usuario_por_id, obtener_todos_los_usuarios
from ...schemas.Seguridad.Usuarios import Usuario, UsuarioBase, UsuarioCreate, UsuarioUpdate
from ...database import get_db


router = APIRouter()

@router.post("/usuarios/")
def crear_usuario(usuario: UsuarioCreate, db: Session = Depends(get_db)):
    try:
        insertar_usuario(db, usuario)
        return {"message": "Usuario insertado correctamente"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
# Endpoint para actualizar una USUARIO existente
@router.put("/usuarios/{id}")
def modificar_usuario(id: int, usuario: UsuarioUpdate, db: Session = Depends(get_db)):
    try:
        actualizar_usuario(db, id, usuario)
        return {"message": "Usuario actualizado correctamente"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
# Endpoint para eliminar una persona
@router.delete("/usuarios/{id}")
def borrar_usuario(id: int, db: Session = Depends(get_db)):
    try:
        db_usuario=eliminar_usuario(db, id)
        if db_usuario is None:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")
        return {"message": "Usuario eliminado correctamente"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
   # Ruta para obtener una usuario por ID 
@router.get("/usuarios/{id}")
def obtener_usuario(id: int, db: Session = Depends(get_db)):
    usuario = obtener_usuario_por_id(db, id)
    return usuario

# Ruta para obtener todas las Usuario
@router.get("/usuarios", response_model=list[Usuario])
def obtener_usuario (skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    usuario = obtener_todos_los_usuarios(db, skip=skip, limit=limit)
    return usuario