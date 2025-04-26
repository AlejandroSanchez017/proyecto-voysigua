from sqlalchemy import Column, String, BigInteger, Text, Numeric, ForeignKey
from app.database import Base

class Sessions(Base):
    __tablename__ = "sessions"

    id = Column(String(255), primary_key=True)
    user_id = Column(BigInteger, ForeignKey("users.id", ondelete="CASCADE"))
    ip_address = Column(String(45), nullable=True)
    user_agent = Column(Text, nullable=True)
    payload = Column(Text, nullable=True)
    last_activity = Column(Numeric, nullable=False)
