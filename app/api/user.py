from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel
from sqlalchemy.orm import Session
from typing import List
from app import crud, schemas, models
from app.core import dependencies, utils
from app.schemas import ErrorCode, ErrorDetail, ErrorResponse
from datetime import timedelta

router = APIRouter(prefix="", tags=["user"])


@router.get(
    "/users/me/",
    response_model=schemas.User,
    responses={
        401: {"model": ErrorResponse},
    },
)
def read_users_me(current_user: models.User = Depends(dependencies.get_current_user)):
    return current_user


@router.post("/users/", response_model=schemas.User)
def create_user(
    user: schemas.UserCreate,
    db: Session = Depends(dependencies.get_db),
    current_user: models.User = Depends(
        dependencies.check_user_role(["superadmin", "admin"]),
    ),
):

    if crud.get_user_by_email(db, email=user.email):
        raise HTTPException(
            status_code=400,
            detail=ErrorDetail.from_error_code(ErrorCode.EMAIL_ALREADY_EXISTS),
        )
    if crud.get_user_by_username(db, username=user.username):
        raise HTTPException(
            status_code=400,
            detail=ErrorDetail.from_error_code(ErrorCode.USERNAME_ALREADY_EXISTS),
        )
    return crud.create_user(db=db, user=user)


@router.get("/users/{user_id}", response_model=schemas.User)
def read_user(
    user_id: int,
    db: Session = Depends(dependencies.get_db),
    current_user: models.User = Depends(
        dependencies.check_user_role(["superadmin", "admin"])
    ),
):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(
            status_code=404,
            detail=ErrorDetail.from_error_code(ErrorCode.USER_NOT_FOUND),
        )
    return db_user


@router.put("/users/{user_id}", response_model=schemas.User)
def update_user(
    user_id: int,
    user: schemas.UserUpdate,
    db: Session = Depends(dependencies.get_db),
    current_user: models.User = Depends(
        dependencies.check_user_role(["superadmin", "admin"])
    ),
):
    db_user = crud.update_user(db, user_id=user_id, user_update=user)
    if db_user is None:
        raise HTTPException(
            status_code=404,
            detail=ErrorDetail.from_error_code(ErrorCode.USER_NOT_FOUND),
        )
    return db_user


@router.delete("/users/{user_id}", response_model=schemas.User)
def delete_user(
    user_id: int,
    db: Session = Depends(dependencies.get_db),
    current_user: models.User = Depends(
        dependencies.check_user_role(["superadmin", "admin"])
    ),
):
    db_user = crud.delete_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(
            status_code=404,
            detail=ErrorDetail.from_error_code(ErrorCode.USER_NOT_FOUND),
        )
    return db_user


@router.get("/users/", response_model=List[schemas.User])
def read_users(
    page: int = Query(1, ge=1),
    per_page: int = Query(10, ge=1, le=100),
    db: Session = Depends(dependencies.get_db),
    current_user: models.User = Depends(
        dependencies.check_user_role(["superadmin", "admin"])
    ),
):
    users = crud.get_users(db, skip=(page - 1) * per_page, limit=per_page)
    return users


class UserChangePassword(BaseModel):
    old_password: str
    new_password: str
    confirm_password: str


@router.put("/users/password/", response_model=schemas.User)
def change_password(
    data: UserChangePassword,
    db: Session = Depends(dependencies.get_db),
    current_user: models.User = Depends(dependencies.get_current_active_user),
):
    if not utils.verify_password(data.old_password, str(current_user.hashed_password)):
        raise HTTPException(
            status_code=400,
            detail=ErrorDetail.from_error_code(ErrorCode.PASSWORD_INCORRECT),
        )
    if data.new_password != data.confirm_password:
        raise HTTPException(
            status_code=400,
            detail=ErrorDetail.from_error_code(ErrorCode.PASSWORD_NOT_MATCH),
        )
    changed_db_user = crud.update_user(
        db=db,
        user_id=current_user.id,  # type: ignore
        user_update=schemas.UserUpdate(
            password=data.new_password,
        ),
    )
    return changed_db_user


class UserChargeRequest(BaseModel):
    key: str


@router.post("/users/charge/", response_model=schemas.User)
def charge_user(
    data: UserChargeRequest,
    db: Session = Depends(dependencies.get_db),
    current_user: models.User = Depends(dependencies.get_current_active_user),
):
    cdkey = crud.get_cdkey_by_key(db, key=data.key)
    if cdkey is None:
        raise HTTPException(
            status_code=404,
            detail=ErrorDetail.from_error_code(ErrorCode.CDKEY_NOT_FOUND),
        )
    if str(cdkey.status) == schemas.CdkeyStatus.used:
        raise HTTPException(
            status_code=400,
            detail=ErrorDetail.from_error_code(ErrorCode.CDKEY_USED),
        )
    if str(cdkey.status) == schemas.CdkeyStatus.expired:
        raise HTTPException(
            status_code=400,
            detail=ErrorDetail.from_error_code(ErrorCode.CDKEY_EXPIRED),
        )

    crud.update_cdkey(db, cdkey_id=cdkey.id, cdkey=schemas.CdkeyUpdate(status=schemas.CdkeyStatus.used))  # type: ignore
    updated_user = crud.update_user(db, user_id=current_user.id, user_update=schemas.UserUpdate(expiration_date=current_user.expiration_date + timedelta(days=cdkey.quota)))  # type: ignore
    return updated_user
