from sqlalchemy import Column, Integer, String
from app.database import Base
from sqlalchemy.orm import relationship
from app.models.Seguridad.role_permissions import role_has_permissions

class Permission(Base):
    __tablename__ = "permissions"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    guard_name = Column(String(100))

    # Relación muchos-a-muchos con Role
    # 'roles' es una lista de objetos Role asociados
    roles = relationship(
        "Role",
        secondary=role_has_permissions,        # Tabla de asociación
        back_populates="permissions",           # Atributo definido en Role
        lazy="selectin"
    )