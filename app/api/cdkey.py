from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel, Field, conint
from sqlalchemy.orm import Session
from typing import List
from app import crud, schemas, models
from app.core import dependencies, utils
from app.schemas import ErrorCode, ErrorDetail

router = APIRouter(prefix="", tags=["cdkeys"])


class GetCdkeyResponse(BaseModel):
    cdkeys: List[schemas.Cdkey]
    total: int


@router.get("/cdkyes", response_model=GetCdkeyResponse)
def read_cdkeys(
    page: int = Query(1, ge=1),
    per_page: int = Query(10, ge=1, le=100),
    db: Session = Depends(dependencies.get_db),
    current_user: models.User = Depends(
        dependencies.check_user_role(["superadmin", "admin"])
    ),
):
    toatl, cdkeys = crud.get_cdkeys(db, page, per_page)
    return {"cdkeys": cdkeys, "total": toatl}


class CreateCdkeyRequest(BaseModel):
    num: int = Field(..., ge=1, le=100)
    quota: int = Field(..., ge=1, le=365)


@router.post("/cdkeys", response_model=List[schemas.Cdkey])
def create_cdkeys(
    cdkey: CreateCdkeyRequest,
    db: Session = Depends(dependencies.get_db),
    current_user: models.User = Depends(
        dependencies.check_user_role(["superadmin", "admin"])
    ),
):
    new_cdkeys_create: List[schemas.CdkeyCreate] = []
    for i in range(cdkey.num):
        new_cdkeys_create.append(
            schemas.CdkeyCreate(key=utils.generate_unique_cdkey(db), quota=cdkey.quota)
        )
    return crud.create_cdkeys(db, new_cdkeys_create)


@router.delete("/cdkeys/{cdkey_id}", response_model=schemas.Cdkey)
def delete_cdkey(
    cdkey_id: int,
    db: Session = Depends(dependencies.get_db),
    current_user: models.User = Depends(
        dependencies.check_user_role(["superadmin", "admin"])
    ),
):
    if (deleted_cdkey := crud.delete_cdkey(db, cdkey_id)) is None:
        raise HTTPException(
            status_code=404,
            detail=ErrorDetail.from_error_code(ErrorCode.CDKEY_NOT_FOUND),
        )
    return deleted_cdkey


@router.get("/cdkeys/{cdkey_id}", response_model=schemas.Cdkey)
def read_cdkey(
    cdkey_id: int,
    db: Session = Depends(dependencies.get_db),
    current_user: models.User = Depends(
        dependencies.check_user_role(["superadmin", "admin"])
    ),
):
    if (cdkey := crud.get_cdkey(db, cdkey_id)) is None:
        raise HTTPException(
            status_code=404,
            detail=ErrorDetail.from_error_code(ErrorCode.CDKEY_NOT_FOUND),
        )
    return cdkey


class UpdateCdkeyRequest(BaseModel):
    quota: int = Field(..., ge=1, le=365)
    status: schemas.CdkeyStatus


@router.put("/cdkeys/{cdkey_id}", response_model=schemas.Cdkey)
def update_cdkey(
    cdkey_id: int,
    cdkey: UpdateCdkeyRequest,
    db: Session = Depends(dependencies.get_db),
    current_user: models.User = Depends(
        dependencies.check_user_role(["superadmin", "admin"])
    ),
):
    if (
        updated_cdkey := crud.update_cdkey(
            db, cdkey_id, schemas.CdkeyUpdate(**cdkey.model_dump())
        )
    ) is None:
        raise HTTPException(
            status_code=404,
            detail=ErrorDetail.from_error_code(ErrorCode.CDKEY_NOT_FOUND),
        )
    return updated_cdkey
