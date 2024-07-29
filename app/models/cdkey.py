import enum
from sqlalchemy import Column, Integer, String, Boolean, DateTime, func, Enum
from app.core.database import Base


class Cdkey(Base):
    __tablename__ = "cdkeys"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    key = Column(String(255), unique=True, index=True, nullable=False)
    status = Column(String(50), default="active")
    quota = Column(Integer, default=30)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
