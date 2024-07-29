import enum
from sqlalchemy import Column, Integer, String, Boolean, DateTime, func, Enum
from app.core.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    full_name = Column(String(100))
    disabled = Column(Boolean, default=False, nullable=False)
    role = Column(String(50), nullable=False, default="user")
    expiration_date = Column(
        DateTime,
        nullable=False,
        default= func.now(),
    )
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
