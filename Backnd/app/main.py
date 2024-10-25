from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from .database import get_db
from sqlalchemy.sql import text  # Esta línea es necesaria para importar 'text'
from .routers.Personas import personas, empleados

app = FastAPI()

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


@app.get("/")
def read_root():
    return {"message": "Bienvenido a la API"}
