import jwt
from datetime import datetime, timedelta
from typing import Optional
from pydantic import BaseModel
from app.core.config import CONFIG


class TokenData(BaseModel):
    username: str


class Token(BaseModel):
    access_token: str
    token_type: str
    expire_at: datetime


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now() + expires_delta
    else:
        expire = datetime.now() + timedelta(minutes=CONFIG.JWT.EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, CONFIG.JWT.SECRET_KEY, algorithm=CONFIG.JWT.ALGORITHM
    )
    return encoded_jwt


def verify_access_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(
            token, CONFIG.JWT.SECRET_KEY, algorithms=[CONFIG.JWT.ALGORITHM]
        )
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except jwt.PyJWTError:
        raise credentials_exception
    return token_data
