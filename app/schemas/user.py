import enum
from pydantic import BaseModel, EmailStr
from datetime import datetime


class RoleOpthons(str, enum.Enum):
    superadmin = "superadmin"
    admin = "admin"
    user = "user"


class UserBase(BaseModel):
    username: str
    email: EmailStr
    expiration_date: datetime | None = None
    full_name: str | None = None
    disabled: bool | None = None
    role: RoleOpthons | None = None


class UserCreate(UserBase):
    password: str


class UserUpdate(UserBase):
    username: str | None = None
    email: EmailStr | None = None
    password: str | None = None
    expiration_date: datetime | None = None


class UserInDBBase(UserBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class User(UserInDBBase):
    pass


class UserInDB(UserInDBBase):
    hashed_password: str
