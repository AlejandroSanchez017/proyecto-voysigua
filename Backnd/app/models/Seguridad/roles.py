from sqlalchemy import Column, Integer, String
from app.database import Base
from sqlalchemy.orm import relationship
from app.models.Seguridad.role_permissions import role_has_permissions

class Role(Base):
    __tablename__ = "roles"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    guard_name = Column(String(100))
    status = Column(String(50))

    # Relación muchos-a-muchos con Permission
    # 'permissions' es una lista de objetos Permission asociados
    permissions = relationship(
        "Permission",
        secondary=role_has_permissions,
        back_populates="roles",
        lazy="selectin"
    )
