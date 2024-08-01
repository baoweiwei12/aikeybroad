from fastapi import APIRouter, Depends, HTTPException, Path, Query
from pydantic import BaseModel
from sqlalchemy.orm import Session
from typing import List, Literal, Required, TypedDict, Union, Sequence
from app import crud, schemas, models
from app.core import dependencies, utils
from app.schemas import ErrorCode, ErrorDetail
from datetime import timedelta

router = APIRouter(prefix="", tags=["config"])


@router.get("/config/doubao_glm/{id}", response_model=schemas.ApiConfigDouBaoGLM)
def get_api_config_doubao_glm(
    id: int,
    db: Session = Depends(dependencies.get_db),
    current_user: models.User = Depends(
        dependencies.check_user_role(["admin", "superadmin"])
    ),
):
    api_config = crud.get_api_config_doubao_glm(db, id)
    if api_config is None:
        raise HTTPException(
            status_code=404,
            detail=ErrorDetail.from_error_code(ErrorCode.API_CONFIG_NOT_FOUND),
        )
    return api_config


@router.get("/config/doubao_glm", response_model=List[schemas.ApiConfigDouBaoGLM])
def get_api_config_doubao_glm_by_page(
    db: Session = Depends(dependencies.get_db),
    current_user: models.User = Depends(
        dependencies.check_user_role(["admin", "superadmin"])
    ),
    page: int = Query(1, ge=1),
    per_page: int = Query(10, ge=1, le=100),
):
    api_configs = crud.get_api_config_doubao_glm_by_page(db, page, per_page)
    return api_configs


@router.post("/config/doubao_glm", response_model=schemas.ApiConfigDouBaoGLM)
def create_api_config_doubao_glm(
    api_config: schemas.ApiConfigDouBaoGLMCreate,
    db: Session = Depends(dependencies.get_db),
    current_user: models.User = Depends(
        dependencies.check_user_role(["admin", "superadmin"])
    ),
):
    api_config = crud.create_api_config_doubao_glm(db, api_config)
    return api_config


@router.put("/config/doubao_glm/{id}", response_model=schemas.ApiConfigDouBaoGLM)
def update_api_config_doubao_glm(
    id: int,
    api_config: schemas.ApiConfigDouBaoGLMUpdate,
    db: Session = Depends(dependencies.get_db),
    current_user: models.User = Depends(
        dependencies.check_user_role(["admin", "superadmin"])
    ),
):

    api_config = crud.update_api_config_doubao_glm(db, id, api_config)
    if api_config is None:
        raise HTTPException(
            status_code=404,
            detail=ErrorDetail.from_error_code(ErrorCode.API_CONFIG_NOT_FOUND),
        )
    return api_config


@router.get("/config/xunfei_ai_ppt/{id}", response_model=schemas.ApiConfigXunFeiAiPPT)
def get_api_config_xunfei_ai_ppt(
    id: int,
    db: Session = Depends(dependencies.get_db),
    current_user: models.User = Depends(
        dependencies.check_user_role(["admin", "superadmin"])
    ),
):
    new_api_config = crud.get_api_config_xunfei_ai_ppt(db, id)

    if new_api_config is None:
        raise HTTPException(
            status_code=404,
            detail=ErrorDetail.from_error_code(ErrorCode.API_CONFIG_NOT_FOUND),
        )
    return new_api_config


@router.get("/config/xunfei_ai_ppt", response_model=List[schemas.ApiConfigXunFeiAiPPT])
def get_api_config_xunfei_ai_ppt_by_page(
    db: Session = Depends(dependencies.get_db),
    current_user: models.User = Depends(
        dependencies.check_user_role(["admin", "superadmin"])
    ),
    page: int = Query(1, ge=1),
    per_page: int = Query(10, ge=1, le=100),
):
    api_configs = crud.get_api_config_xunfei_ai_ppt_by_page(db, page, per_page)
    return api_configs


@router.post("/config/xunfei_ai_ppt", response_model=schemas.ApiConfigXunFeiAiPPT)
def create_api_config_xunfei_ai_ppt(
    api_config: schemas.ApiConfigXunFeiAiPPTCreate,
    db: Session = Depends(dependencies.get_db),
    current_user: models.User = Depends(
        dependencies.check_user_role(["admin", "superadmin"])
    ),
):
    api_config = crud.create_api_config_xunfei_ai_ppt(db, api_config)
    return api_config


@router.put("/config/xunfei_ai_ppt/{id}", response_model=schemas.ApiConfigXunFeiAiPPT)
def update_api_config_xunfei_ai_ppt(
    id: int,
    api_config: schemas.ApiConfigXunFeiAiPPTUpdate,
    db: Session = Depends(dependencies.get_db),
    current_user: models.User = Depends(
        dependencies.check_user_role(["admin", "superadmin"])
    ),
):
    new_api_config = crud.update_api_config_xunfei_ai_ppt(db, id, api_config)
    if new_api_config is None:
        raise HTTPException(
            status_code=404,
            detail=ErrorDetail.from_error_code(ErrorCode.API_CONFIG_NOT_FOUND),
        )
    return new_api_config


@router.get(
    "/api_config/bytedance_openspeech/{id}",
    response_model=schemas.ApiConfigByteDanceOpenspeech,
)
def get_api_config_bytedance_openspeech(
    id: int,
    db: Session = Depends(dependencies.get_db),
    current_user: models.User = Depends(
        dependencies.check_user_role(["admin", "superadmin"])
    ),
):
    api_config = crud.get_api_config_bytedance_openspeech(db, id)
    if api_config is None:
        raise HTTPException(
            status_code=404,
            detail=ErrorDetail.from_error_code(ErrorCode.API_CONFIG_NOT_FOUND),
        )
    return api_config


@router.get(
    "/api_config/bytedance_openspeech",
    response_model=List[schemas.ApiConfigByteDanceOpenspeech],
)
def get_api_config_bytedance_openspeech_by_page(
    db: Session = Depends(dependencies.get_db),
    current_user: models.User = Depends(
        dependencies.check_user_role(["admin", "superadmin"])
    ),
    page: int = Query(1, ge=1),
    per_page: int = Query(10, ge=1, le=100),
):
    api_configs = crud.get_api_config_bytedance_openspeech_by_page(db, page, per_page)
    return api_configs


@router.post(
    "/api_config/bytedance_openspeech",
    response_model=schemas.ApiConfigByteDanceOpenspeech,
)
def create_api_config_bytedance_openspeech(
    api_config: schemas.ApiConfigByteDanceOpenspeechCreate,
    db: Session = Depends(dependencies.get_db),
    current_user: models.User = Depends(
        dependencies.check_user_role(["admin", "superadmin"])
    ),
):
    api_config = crud.create_api_config_bytedance_openspeech(db, api_config)
    return api_config


@router.put(
    "/api_config/bytedance_openspeech/{id}",
    response_model=schemas.ApiConfigByteDanceOpenspeech,
)
def update_api_config_bytedance_openspeech(
    id: int,
    api_config: schemas.ApiConfigByteDanceOpenspeechUpdate,
    db: Session = Depends(dependencies.get_db),
    current_user: models.User = Depends(
        dependencies.check_user_role(["admin", "superadmin"])
    ),
):
    api_config = crud.update_api_config_bytedance_openspeech(db, id, api_config)
    if api_config is None:
        raise HTTPException(
            status_code=404,
            detail=ErrorDetail.from_error_code(ErrorCode.API_CONFIG_NOT_FOUND),
        )
    return api_config
