from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from app.schemas.Seguridad.Sesiones import SesionCreate, SesionResponse, SesionUsuarioResponse, SesionInactivaResponse
import logging

logger = logging.getLogger(__name__)

async def insertar_sesion(db: AsyncSession, sesion: SesionCreate):
    query = text("""
        CALL insertar_sesion(:id, :user_id, :ip_address, :user_agent, :payload, :last_activity)
    """)

    try:
        async with db.begin():
            await db.execute(query, {
                "id": sesion.id,
                "user_id": sesion.user_id,
                "ip_address": sesion.ip_address,
                "user_agent": sesion.user_agent,
                "payload": sesion.payload,
                "last_activity": sesion.last_activity
            })
        await db.commit()
        return {"message": f"Sesión '{sesion.id}' insertada correctamente"}
    except Exception as e:
        logger.error(f"Error al insertar sesión: {e}")
        raise

async def eliminar_sesion(db: AsyncSession, id: str):
    query = text("CALL eliminar_sesion(:id)")

    try:
        async with db.begin():
            await db.execute(query, {"id": id})
        await db.commit()
        return {"message": f"Sesión con ID {id} eliminada correctamente"}
    except Exception as e:
        logger.error(f"Error al eliminar sesión: {e}")
        raise

async def consultar_sesion_por_id(db: AsyncSession, id: str) -> SesionResponse:
    query = text("""
        SELECT id, user_id, ip_address, user_agent, payload, last_activity
        FROM sessions
        WHERE id = :id
    """)

    try:
        result = await db.execute(query, {"id": id})
        row = result.fetchone()

        if not row:
            raise ValueError(f"No se encontró la sesión con ID {id}")

        return SesionResponse(
            id=row[0],
            user_id=row[1],
            ip_address=row[2],
            user_agent=row[3],
            payload=row[4],
            last_activity=row[5]
        )

    except Exception as e:
        logger.error(f"Error al consultar sesión por ID: {e}")
        raise

async def eliminar_sesiones_antiguas(db: AsyncSession, dias_inactividad: int):
    query = text("CALL eliminar_sesiones_antiguas(:dias_inactividad)")

    try:
        async with db.begin():
            await db.execute(query, {"dias_inactividad": dias_inactividad})
        await db.commit()

        return {"message": f"Sesiones inactivas por más de {dias_inactividad} días eliminadas correctamente"}
    except Exception as e:
        logger.error(f"Error al eliminar sesiones antiguas: {e}")
        raise

async def consultar_sesiones_por_usuario(db: AsyncSession, user_id: int) -> list[SesionUsuarioResponse]:
    query = text("""
        SELECT id, ip_address, user_agent, last_activity
        FROM sessions
        WHERE user_id = :user_id
    """)

    try:
        result = await db.execute(query, {"user_id": user_id})
        rows = result.fetchall()

        if not rows:
            raise ValueError(f"No se encontraron sesiones para el usuario con ID {user_id}")

        return [
            SesionUsuarioResponse(
                id=row[0],
                ip_address=row[1],
                user_agent=row[2],
                last_activity=row[3]
            ) for row in rows
        ]
    except Exception as e:
        logger.error(f"Error al consultar sesiones por usuario: {e}")
        raise

async def cerrar_sesiones_por_usuario(db: AsyncSession, user_id: int):
    query = text("CALL cerrar_sesiones_por_usuario(:user_id)")

    try:
        async with db.begin():
            await db.execute(query, {"user_id": user_id})
        await db.commit()

        return {"message": f"Todas las sesiones del usuario con ID {user_id} fueron cerradas correctamente"}
    except Exception as e:
        logger.error(f"Error al cerrar sesiones por usuario: {e}")
        raise

async def consultar_sesiones_inactivas(db: AsyncSession, intervalo: str) -> list[SesionInactivaResponse]:
    # Construcción del intervalo directamente en SQL
    query = text(f"""
        SELECT id, user_id, last_activity,
        NOW() - TO_TIMESTAMP(last_activity) AS tiempo_inactividad
        FROM sessions
        WHERE NOW() - TO_TIMESTAMP(last_activity) >= INTERVAL '{intervalo}'
    """)

    try:
        result = await db.execute(query)
        rows = result.fetchall()

        if not rows:
            raise ValueError("No se encontraron sesiones inactivas")

        def formatear_intervalo(intervalo_pg):
            dias = intervalo_pg.days
            segundos = intervalo_pg.seconds
            horas = segundos // 3600
            minutos = (segundos % 3600) // 60
            if dias > 0:
                return f"{dias} días"
            elif horas > 0:
                return f"{horas} horas"
            elif minutos > 0:
                return f"{minutos} minutos"
            else:
                return f"{int(segundos)} segundos"

        sesiones = []
        for row in rows:
            sesiones.append(SesionInactivaResponse(
                id=row[0],
                user_id=row[1],
                last_activity=row[2],
                tiempo_inactividad=formatear_intervalo(row[3])
            ))

        return sesiones

    except Exception as e:
        logger.error(f"Error al consultar sesiones inactivas: {e}")
        raise

async def eliminar_sesiones_inactivas(db: AsyncSession, intervalo: str):
    query = text(f"""
        CALL eliminar_sesiones_inactivas(INTERVAL '{intervalo}')
    """)
    try:
        async with db.begin():
            await db.execute(query)
        await db.commit()
        return {"message": f"Sesiones inactivas desde {intervalo} eliminadas correctamente"}
    except Exception as e:
        logger.error(f"Error al eliminar sesiones inactivas: {e}")
        raise  