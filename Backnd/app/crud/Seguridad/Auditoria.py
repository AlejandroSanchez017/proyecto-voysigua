from sqlalchemy.orm import Session
from app.models.Seguridad.Auditoria import Auditoria
from typing import List

def obtener_registros_auditoria(db: Session, skip: int = 0, limit: int = 10) -> List[Auditoria]:
    return (
        db.query(Auditoria)
          .order_by(Auditoria.fecha.desc())
          .offset(skip)
          .limit(limit)
          .all()
    )

def obtener_auditoria_por_id(db: Session, id_auditoria: int) -> Auditoria | None:
    return (
        db.query(Auditoria)
          .filter(Auditoria.idauditoria == id_auditoria)
          .first()
    )


def obtener_auditorias_por_tipo(
    db: Session,
    tipo: str,
    skip: int = 0,
    limit: int = 10
) -> List[Auditoria]:
    return (
        db.query(Auditoria)
        .filter(Auditoria.tipo == tipo)
        .order_by(Auditoria.fecha.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )

def obtener_auditorias_por_tabla(
    db: Session,
    tabla: str,
    skip: int = 0,
    limit: int = 10
) -> List[Auditoria]:
    return (
        db.query(Auditoria)
        .filter(Auditoria.tabla.ilike(tabla))
        .order_by(Auditoria.fecha.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )

def obtener_auditorias_por_usuario(
    db: Session,
    usuario: str,
    skip: int = 0,
    limit: int = 10
) -> List[Auditoria]:
    return (
        db.query(Auditoria)
        .filter(Auditoria.usuario.ilike(usuario))
        .order_by(Auditoria.fecha.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )
