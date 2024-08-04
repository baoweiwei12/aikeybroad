import enum
from sqlalchemy import Column, Integer, String, Boolean, DateTime, func, Enum, JSON,ForeignKey,Text
from app.core.database import Base
from .user import User

class AiChatMessage(Base):
    __tablename__ = "ai_chat_messages"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer,ForeignKey(User.id),index=True, nullable=False,)
    role = Column(String(20), nullable=False)
    content = Column(Text, nullable=False)