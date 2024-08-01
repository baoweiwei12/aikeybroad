from datetime import datetime
from enum import Enum
from pydantic import BaseModel


class ApiConfigDouBaoGLMCreate(BaseModel):
    name: str
    api_key: str
    model: str


class ApiConfigDouBaoGLMUpdate(BaseModel):
    name: str | None = None
    api_key: str | None = None
    model: str | None = None
    enabled: bool | None = None


class ApiConfigDouBaoGLM(BaseModel):
    id: int
    name: str
    api_key: str
    model: str
    enabled: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class ApiConfigXunFeiAiPPTCreate(BaseModel):
    name: str
    api_secret: str
    app_id: str


class ApiConfigXunFeiAiPPTUpdate(BaseModel):
    name: str | None = None
    api_secret: str | None = None
    app_id: str | None = None
    enabled: bool | None = None


class ApiConfigXunFeiAiPPT(BaseModel):
    id: int
    name: str
    api_secret: str
    app_id: str
    enabled: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class ApiConfigByteDanceOpenspeechCreate(BaseModel):
    name: str
    appid: str
    token: str
    cluster: str


class ApiConfigByteDanceOpenspeechUpdate(BaseModel):
    name: str | None = None
    appid: str | None = None
    token: str | None = None
    cluster: str | None = None
    enabled: bool | None = None


class ApiConfigByteDanceOpenspeech(BaseModel):
    id: int
    name: str
    appid: str
    token: str
    cluster: str
    enabled: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
