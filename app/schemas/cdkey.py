import enum
from pydantic import BaseModel
from datetime import datetime


class CdkeyStatus(str, enum.Enum):
    active = "active"
    used = "used"
    expired = "expired"


class CdkeyBase(BaseModel):
    key: str


class CdkeyCreate(CdkeyBase):
    quota: int | None = None


class CdkeyUpdate(BaseModel):
    status: CdkeyStatus | None = None
    quota: int | None = None


class Cdkey(CdkeyBase):
    id: int
    key: str
    quota: int
    status: CdkeyStatus
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
