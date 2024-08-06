import enum
from fastapi import APIRouter, Depends, HTTPException, Path, Query
from fastapi.exceptions import RequestValidationError
from pydantic import BaseModel, ValidationError
from sqlalchemy.orm import Session
from typing import List, Literal, Required, TypedDict, Union, Sequence
from app import crud, schemas, models
from app.core import dependencies, utils
from app.schemas import ErrorCode, ErrorDetail
from datetime import timedelta

router = APIRouter(prefix="", tags=["config"])


class ApiConfigType(enum.Enum):
    doubao_glm = "doubao_glm"
    xunfei_ai_ppt = "xunfei_ai_ppt"
    bytedance_openspeech = "bytedance_openspeech"


GET_CONFIG_BY_ID_MAP = {
    ApiConfigType.doubao_glm: crud.get_api_config_doubao_glm,
    ApiConfigType.xunfei_ai_ppt: crud.get_api_config_xunfei_ai_ppt,
    ApiConfigType.bytedance_openspeech: crud.get_api_config_bytedance_openspeech,
}

GET_CONFIG_BY_PAGE_MAP = {
    ApiConfigType.doubao_glm: crud.get_api_config_doubao_glm_by_page,
    ApiConfigType.xunfei_ai_ppt: crud.get_api_config_xunfei_ai_ppt_by_page,
    ApiConfigType.bytedance_openspeech: crud.get_api_config_bytedance_openspeech_by_page,
}


@router.get(
    "/config",
    response_model=Union[
        schemas.ApiConfigDouBaoGLM,
        schemas.ApiConfigXunFeiAiPPT,
        schemas.ApiConfigByteDanceOpenspeech,
    ],
)
def get_api_config(
    type: ApiConfigType = Query("doubao_glm"),
    id: int = Query(...),
    db=Depends(dependencies.get_db),
    current_user=Depends(dependencies.check_user_role(["admin", "superadmin"])),
):
    result = GET_CONFIG_BY_ID_MAP[type](db, id)
    if result is None:
        raise HTTPException(
            status_code=404,
            detail=ErrorDetail.from_error_code(ErrorCode.API_CONFIG_NOT_FOUND),
        )
    return result


@router.get(
    "/config/list",
    response_model=List[
        schemas.ApiConfigDouBaoGLM
        | schemas.ApiConfigXunFeiAiPPT
        | schemas.ApiConfigByteDanceOpenspeech
    ],
)
def get_api_config_by_page(
    type: ApiConfigType = Query("doubao_glm"),
    page: int = Query(1, ge=1),
    per_page: int = Query(10, ge=1, le=100),
    db=Depends(dependencies.get_db),
    current_user=Depends(dependencies.check_user_role(["admin", "superadmin"])),
):
    return GET_CONFIG_BY_PAGE_MAP[type](db, page, per_page)


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


@router.post(
    "/config/bytedance_openspeech",
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
    "/config/bytedance_openspeech/{id}",
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
