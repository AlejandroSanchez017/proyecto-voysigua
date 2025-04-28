from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.database import get_sync_db
from app.crud.Seguridad.Auditoria import obtener_registros_auditoria, obtener_auditoria_por_id, obtener_auditorias_por_tipo, obtener_auditorias_por_tabla, obtener_auditorias_por_usuario
from app.schemas.Seguridad.Auditoria import AuditoriaResponse
from typing import List
from fastapi import APIRouter

router = APIRouter()

@router.get("/auditoria/", response_model=List[AuditoriaResponse])
def listar_auditoria(
    db: Session = Depends(get_sync_db)
):
    registros = obtener_registros_auditoria(db)
    if not registros:
        raise HTTPException(status_code=404, detail="No se encontraron registros de auditoría")
    return registros

@router.get("/auditoria/{id_auditoria}", response_model=AuditoriaResponse)
def buscar_auditoria_por_id(
    id_auditoria: int,
    db: Session = Depends(get_sync_db)
):
    registro = obtener_auditoria_por_id(db, id_auditoria)
    if not registro:
        raise HTTPException(status_code=404, detail=f"No se encontró auditoría con ID {id_auditoria}")
    return registro

@router.get("/auditoria/tipo/{tipo}", response_model=List[AuditoriaResponse])
def listar_auditoria_por_tipo(
    tipo: str,
    skip: int = Query(0, ge=0, description="Registros a omitir"),
    limit: int = Query(10, gt=0, le=100, description="Máximo de registros a retornar"),
    db: Session = Depends(get_sync_db)
):
    tipo = tipo.upper()
    if tipo not in ("I", "U", "D"):
        raise HTTPException(
            status_code=400,
            detail="El tipo debe ser 'I' (INSERT), 'U' (UPDATE) o 'D' (DELETE)"
        )

    auditorias = obtener_auditorias_por_tipo(db, tipo, skip, limit)
    if not auditorias:
        raise HTTPException(status_code=404, detail=f"No se encontraron registros con tipo '{tipo}'")
    return auditorias

@router.get("/auditoria/tabla/{tabla}", response_model=List[AuditoriaResponse])
def listar_auditoria_por_tabla(
    tabla: str,
    skip: int = Query(0, ge=0, description="Registros a omitir"),
    limit: int = Query(10, gt=0, le=100, description="Máximo de registros a retornar"),
    db: Session = Depends(get_sync_db)
):
    auditorias = obtener_auditorias_por_tabla(db, tabla, skip, limit)
    if not auditorias:
        raise HTTPException(status_code=404, detail=f"No se encontraron registros de auditoría para la tabla '{tabla}'")
    return auditorias

@router.get("/auditoria/usuario/{usuario}", response_model=List[AuditoriaResponse])
def listar_auditoria_por_usuario(
    usuario: str,
    skip: int = Query(0, ge=0, description="Registros a omitir"),
    limit: int = Query(10, gt=0, le=100, description="Máximo de registros a retornar"),
    db: Session = Depends(get_sync_db)
):
    auditorias = obtener_auditorias_por_usuario(db, usuario, skip, limit)
    if not auditorias:
        raise HTTPException(status_code=404, detail=f"No se encontraron registros para el usuario '{usuario}'")
    return auditorias
