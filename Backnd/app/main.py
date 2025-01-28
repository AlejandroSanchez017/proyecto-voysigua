from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from .database import get_db
from sqlalchemy.sql import text  # Esta línea es necesaria para importar 'text'
from .routers.Personas import personas, empleados
from .routers.Seguridad import Usuario
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

origins = ["http://localhost:3000"],  # URL de tu aplicación React en modo desarrollo ]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Cambia esto según el origen de tu aplicación frontend
    allow_credentials=True,
    allow_methods=["*"],  # Puedes restringir métodos si es necesario
    allow_headers=["*"],
)

# Ruta para probar la conexión a la base de datos
@app.get("/test-db")
def test_db(db: Session = Depends(get_db)):
    try:
        # Ejecutamos una consulta simple para verificar la conexión
        db.execute(text("SELECT 1"))
        return {"message": "Conexión exitosa a la base de datos"}
    except Exception as e:
        return {"error": str(e)}

# Incluir los routers en la aplicación principal
app.include_router(personas.router)
app.include_router(empleados.router)
app.include_router(Usuario.router)


@app.get("/")
def read_root():
    return {"message": "Bienvenido a la API"}

