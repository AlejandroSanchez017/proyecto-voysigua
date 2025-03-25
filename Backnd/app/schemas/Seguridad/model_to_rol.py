from pydantic import BaseModel

class AsignarRolRequest(BaseModel):
    role_id: int
    tipo_modelo: str  # antes: model_type
    id_modelo: int    # antes: model_id
