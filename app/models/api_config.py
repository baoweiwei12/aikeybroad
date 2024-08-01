import enum
from sqlalchemy import Column, Integer, String, Boolean, DateTime, func, Enum, JSON
from app.core.database import Base


class ApiConfigDouBaoGLM(Base):
    __tablename__ = "api_config_doubao_glm"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    api_key = Column(String(255), nullable=False)
    model = Column(String(255), nullable=False)
    enabled = Column(Boolean, default=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())


class ApiConfigXunFeiAiPPT(Base):
    __tablename__ = "api_config_xunfei_ai_ppt"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    app_id = Column(String(255), nullable=False)
    api_secret = Column(String(255), nullable=False)
    enabled = Column(Boolean, default=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())


class ApiConfigBytedanceOpenspeech(Base):
    __tablename__ = "api_config_bytedance_openspeech"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    appid = Column(String(255), nullable=False)
    token = Column(String(255), nullable=False)
    cluster = Column(String(255), nullable=False)
    enabled = Column(Boolean, default=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
