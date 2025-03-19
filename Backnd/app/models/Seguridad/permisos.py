from sqlalchemy import Column, Integer, String
from app.database import Base

class Permission(Base):
    __tablename__ = "permissions"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    guard_name = Column(String(100))
