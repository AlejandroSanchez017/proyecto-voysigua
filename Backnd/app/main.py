from fastapi import FastAPI, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import  get_async_db, get_sync_db# Importamos las funciones correctas
from sqlalchemy.sql import text
from app.routers.Personas import personas, empleados
from app.routers.mandados_paquetes import mandados
from app.routers.Personas import (direcciones, personas, empleados, telefonos)
from app.routers.Seguridad import (Usuario, roles as roles_router, permisos as permisos_router, 
                                   role_permissions as role_permissions_router, model_to_rol, 
                                   model_to_permission, parametros as parametros_router, 
                                   objeto as objeto_router,  Sesiones as sesiones_router, Auditoria as auditoria_router)
from app.routers.Seguridad.Autenticacion import router as auth_routes
from fastapi.middleware.cors import CORSMiddleware
import os



import sys
import locale
import uvicorn


app = FastAPI()

# Obtener el origen desde variable de entorno
frontend_origin = os.getenv("FRONTEND_ORIGIN")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[frontend_origin] if frontend_origin else [],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



# Manejo seguro de codificación de consola
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

# Manejo seguro de configuración regional
try:
    locale.setlocale(locale.LC_ALL, "es_ES.UTF-8")
except locale.Error:
    locale.setlocale(locale.LC_ALL, "")

# Registrar rutas
app.include_router(auth_routes, prefix="/auth")
app.include_router(personas.router)
app.include_router(empleados.router)
app.include_router(Usuario.router)
app.include_router(mandados.router)
app.include_router(roles_router.router)
app.include_router(permisos_router.router, tags=["Permisos"])
app.include_router(role_permissions_router.router, tags=["Permisos-Roles"])
app.include_router(model_to_rol.router, tags=["Roles-Modelos"])
app.include_router(model_to_permission.router, tags=["Permisos-Modelos"])
app.include_router(telefonos.router, tags=["Tipos de Teléfono"])
app.include_router(direcciones.router, tags=["Departamentos"])
app.include_router(objeto_router.router, tags=["objetos"])
app.include_router(parametros_router.router, tags=["parametros"])
app.include_router(sesiones_router.router,  tags=["Sesiones"])
app.include_router(auditoria_router.router, tags=["Auditoría"])



@app.get("/")
async def read_root():
    return {"message": "Bienvenido a la API"}

# Ruta de prueba de conexión (ASÍNCRONA)
@app.get("/test-db")
async def test_db(db: AsyncSession = Depends(get_async_db)):  # Cambiado a get_async_db
    try:
        await db.execute(text("SELECT 1"))
        return {"message": "Conexión exitosa a la base de datos"}
    except Exception as e:
        return {"error": str(e)}

# Iniciar la aplicación con Uvicorn
if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=5000, reload=True)
