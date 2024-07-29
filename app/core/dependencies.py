from datetime import datetime
from typing import List
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from app.core.security import verify_access_token
from app import crud, models, schemas
from app.core.database import SessionLocal
from sqlalchemy.orm import Session


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/login/token")


def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=schemas.ErrorDetail.from_error_code(
            schemas.ErrorCode.TOKEN_VALIDATION_ERROR
        ),
        headers={"WWW-Authenticate": "Bearer"},
    )
    token_data = verify_access_token(token, credentials_exception)
    user = crud.get_user_by_username(db, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user


def get_current_active_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=schemas.ErrorDetail.from_error_code(
            schemas.ErrorCode.TOKEN_VALIDATION_ERROR
        ),
        headers={"WWW-Authenticate": "Bearer"},
    )
    token_data = verify_access_token(token, credentials_exception)
    user = crud.get_user_by_username(db, username=token_data.username)
    if user is None:
        raise credentials_exception
    if bool(user.disabled):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=schemas.ErrorDetail.from_error_code(
                schemas.ErrorCode.ACCOUNT_DISABLED
            ),
        )
    return user


def check_user_role(required_roles: List[str]):
    def role_checker(current_user: models.User = Depends(get_current_active_user)):
        if current_user.role not in required_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=schemas.ErrorDetail.from_error_code(
                    schemas.ErrorCode.PERMISSION_DENIED
                ),
            )
        return current_user

    return role_checker


def check_is_expired(
    current_user: models.User = Depends(get_current_active_user),
):
    is_expired: bool = bool(current_user.expiration_date < datetime.now())
    if is_expired:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=schemas.ErrorDetail.from_error_code(schemas.ErrorCode.IS_EXPIRED),
        )
    return is_expired
