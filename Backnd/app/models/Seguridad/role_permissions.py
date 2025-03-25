from sqlalchemy import Table, Column, Integer, ForeignKey
from app.database import Base

role_has_permissions = Table(
    "role_has_permissions",
    Base.metadata,
    Column("permission_id", Integer, ForeignKey("permissions.id", ondelete="CASCADE"), primary_key=True),
    Column("role_id", Integer, ForeignKey("roles.id", ondelete="CASCADE"), primary_key=True),
)