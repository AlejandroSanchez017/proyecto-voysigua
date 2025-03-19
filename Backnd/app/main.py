from fastapi import FastAPI, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_sync_db, get_async_db  # ✅ Importamos las funciones correctas
from sqlalchemy.sql import text
from app.routers.Personas import personas, empleados
from app.routers.Seguridad import Usuario, roles as roles_router, permisos as permisos_router
from app.routers.Seguridad.Autenticacion import router as auth_routes
from fastapi.middleware.cors import CORSMiddleware
import sys
import locale
import uvicorn

app = FastAPI()

# Middleware de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


sys.stdout.reconfigure(encoding="utf-8")
locale.setlocale(locale.LC_ALL, "es_ES.UTF-8")

# Registrar rutas
app.include_router(auth_routes, prefix="/auth")
app.include_router(personas.router)
app.include_router(empleados.router)
app.include_router(Usuario.router)
app.include_router(roles_router.router)
app.include_router(permisos_router.router, tags=["Permisos"])

@app.get("/")
async def read_root():
    return {"message": "Bienvenido a la API"}

# Ruta de prueba de conexión (ASÍNCRONA)
@app.get("/test-db")
async def test_db(db: AsyncSession = Depends(get_async_db)):  # ✅ Cambiado a get_async_db
    try:
        await db.execute(text("SELECT 1"))
        return {"message": "Conexión exitosa a la base de datos"}
    except Exception as e:
        return {"error": str(e)}

# Iniciar la aplicación con Uvicorn
if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=5000, reload=True)
