from sqlalchemy.orm import Session
from sqlalchemy.sql import text
from ...schemas.Seguridad.Usuarios import UsuarioCreate, UsuarioUpdate
from ...models.Seguridad.Usuarios import Usuario

# Insertar usuario llamando a procedimiento almacenado
def insertar_usuario(db: Session, usuario: UsuarioCreate):
    query = text("""
        CALL insertar_usuario(:cod_persona, :nombre, :password, :remember_token, 
                               :username, :preguntas_contestadas, :estado, :primera_vez, :fecha_vencimiento,
                                :intentos_preguntas, :preguntas_correctas)
    """)
    db.execute(query, {
        "cod_persona": usuario.cod_persona,
        "nombre": usuario.nombre,
        "password": usuario.password,
        "remember_token": usuario.remember_token,
        "username": usuario.username,
        "preguntas_contestadas": usuario.preguntas_contestadas,
        "estado": usuario.estado,
        "primera_vez": usuario.primera_vez,
        "fecha_vencimiento": usuario.fecha_vencimiento,
        "intentos_preguntas": usuario.intentos_preguntas,
        "preguntas_correctas": usuario.preguntas_correctas
    })
    db.commit()

# Actualizar usuario
def actualizar_usuario(db: Session, id: int, usuario: UsuarioUpdate):
    query = text("""
        CALL actualizar_usuario(:id, :cod_persona, :nombre, :password, :remember_token, 
                               :username, :preguntas_contestadas, :estado, :primera_vez, :fecha_vencimiento,
                                :intentos_preguntas, :preguntas_correctas)
    """)
    db.execute(query, {
        "id": id,
        "cod_persona": usuario.cod_persona,
        "nombre": usuario.nombre,
        "password": usuario.password,
        "remember_token": usuario.remember_token,
        "username": usuario.username,
        "preguntas_contestadas": usuario.preguntas_contestadas,
        "estado": usuario.estado,
        "primera_vez": usuario.primera_vez,
        "fecha_vencimiento": usuario.fecha_vencimiento,
        "intentos_preguntas": usuario.intentos_preguntas,
        "preguntas_correctas": usuario.preguntas_correctas
    })
    db.commit()

# Eliminar usuario
def eliminar_usuario(db: Session, id: int):
    db_usuario = db.query(Usuario).filter(Usuario.id == id).first()
    if db_usuario:
        db.delete(db_usuario)
        db.commit()
        return db_usuario
    return None

# Obtener usuario por id
def obtener_usuario_por_id(db: Session, id: int):
    return db.query(Usuario).filter(Usuario.id == id).first()

# Obtener todos los usuarios
def obtener_todos_los_usuarios(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Usuario).offset(skip).limit(limit).all()