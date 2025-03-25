from pydantic import BaseModel

class AsignarPermisoRequest(BaseModel):
    permission_id: int
    tipo_modelo: str  # antes: model_type
    id_modelo: int    # antes: model_id