import enum
from sqlalchemy import Column, Integer, String, Boolean, DateTime, func, Enum, JSON,Text,ForeignKey
from app.core.database import Base
from app.models.user import User

class AiPPTRecord(Base):
    __tablename__ = "ai_ppt_records"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey(User.id),nullable=False,)
    text = Column(Text, nullable=False)
    sid = Column(String(255),index=True, nullable=False)
    cover_img_src = Column(String(255), nullable=False)
    sub_title = Column(String(255), nullable=False)
    title = Column(String(255), nullable=False)
    process = Column(Integer, nullable=True,default=0)
    ppt_url = Column(String(255), nullable=True)
    err_msg = Column(String(255), nullable=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    error_count = Column(Integer, nullable=False,default=0)
