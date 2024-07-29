from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel, EmailStr
from sqlalchemy.orm import Session
from app import crud, models, schemas
from app.core import dependencies, security, utils
from datetime import datetime, timedelta
from app.core.config import CONFIG

router = APIRouter(prefix="", tags=["auth"])


@router.post("/login/token", response_model=security.Token)
def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(dependencies.get_db),
):
    user = crud.get_user_by_username(db, form_data.username)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=schemas.ErrorDetail.from_error_code(
                schemas.ErrorCode.ACCOUNT_NOT_FOUND
            ),
            headers={"WWW-Authenticate": "Bearer"},
        )
    if utils.verify_password(form_data.password, str(user.hashed_password)) is False:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=schemas.ErrorDetail.from_error_code(
                schemas.ErrorCode.PASSWORD_INCORRECT
            ),
            headers={"WWW-Authenticate": "Bearer"},
        )
    expires_delta = timedelta(minutes=CONFIG.JWT.EXPIRE_MINUTES)
    access_token = security.create_access_token(
        data={"sub": user.username}, expires_delta=expires_delta
    )
    return security.Token(
        access_token=access_token,
        token_type="bearer",
        expire_at=datetime.now() + expires_delta,
    )


@router.post("/refresh/token", response_model=security.Token)
def refresh_access_token(
    current_user: models.User = Depends(dependencies.get_current_active_user),
    db: Session = Depends(dependencies.get_db),
):
    expires_delta = timedelta(minutes=CONFIG.JWT.EXPIRE_MINUTES)
    access_token = security.create_access_token(
        data={"sub": current_user.username}, expires_delta=expires_delta
    )
    return security.Token(
        access_token=access_token,
        token_type="bearer",
        expire_at=datetime.now() + expires_delta,
    )


class UserRegister(BaseModel):
    username: str
    email: EmailStr
    password: str


@router.post("/register", response_model=schemas.User)
def register_user(
    user: UserRegister,
    db: Session = Depends(dependencies.get_db),
):
    if crud.get_user_by_username(db, username=user.username) or crud.get_user_by_email(
        db, email=user.email
    ):
        raise HTTPException(
            status_code=400,
            detail=schemas.ErrorDetail.from_error_code(
                schemas.ErrorCode.ACCOUNT_ALREADY_EXISTS
            ),
        )
    db_user = crud.create_user(
        db,
        user=schemas.UserCreate(
            username=user.username,
            email=user.email,
            password=user.password,
            role=schemas.RoleOpthons.user,
        ),
    )
    return db_user


class MacAddressAuth(BaseModel):
    mac_address: str


@router.post("/register/mac_addres", response_model=schemas.User)
def register_user_by_mac_address(
    req: MacAddressAuth,
    db: Session = Depends(dependencies.get_db),
):
    if crud.get_user_by_username(db, username=req.mac_address):
        raise HTTPException(
            status_code=400,
            detail=schemas.ErrorDetail.from_error_code(
                schemas.ErrorCode.ACCOUNT_ALREADY_EXISTS
            ),
        )
    db_user = crud.create_user(
        db,
        user=schemas.UserCreate(
            username=req.mac_address,
            email=f"{req.mac_address}@fake.com",
            password=req.mac_address,
            role=schemas.RoleOpthons.user,
        ),
    )
    return db_user


@router.post("/login/token/mac_addres", response_model=security.Token)
def login_for_access_token_by_mac_address(
    req: MacAddressAuth,
    db: Session = Depends(dependencies.get_db),
):
    user = crud.get_user_by_username(db, req.mac_address)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=schemas.ErrorDetail.from_error_code(
                schemas.ErrorCode.ACCOUNT_NOT_FOUND
            ),
            headers={"WWW-Authenticate": "Bearer"},
        )
    if utils.verify_password(req.mac_address, str(user.hashed_password)) is False:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=schemas.ErrorDetail.from_error_code(
                schemas.ErrorCode.PASSWORD_INCORRECT
            ),
            headers={"WWW-Authenticate": "Bearer"},
        )
    expires_delta = timedelta(minutes=CONFIG.JWT.EXPIRE_MINUTES)
    access_token = security.create_access_token(
        data={"sub": user.username}, expires_delta=expires_delta
    )
    return security.Token(
        access_token=access_token,
        token_type="bearer",
        expire_at=datetime.now() + expires_delta,
    )


@router.post("/refresh/token/mac_address", response_model=security.Token)
def refresh_access_token_by_mac_address(
    current_user: models.User = Depends(dependencies.get_current_active_user),
    db: Session = Depends(dependencies.get_db),
):
    expires_delta = timedelta(minutes=CONFIG.JWT.EXPIRE_MINUTES)
    access_token = security.create_access_token(
        data={"sub": current_user.username}, expires_delta=expires_delta
    )
    return security.Token(
        access_token=access_token,
        token_type="bearer",
        expire_at=datetime.now() + expires_delta,
    )