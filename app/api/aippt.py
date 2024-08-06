import logging
import time
from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, Path, Query
from pydantic import BaseModel
from sqlalchemy.orm import Session
from typing import List, Literal, Required, TypedDict, Union, Sequence
from app import crud, schemas, models
from app.core import dependencies, utils
from app.schemas import ErrorCode, ErrorDetail
from datetime import timedelta
from app.service import xunfei_aippt
from app import crud, schemas, models

router = APIRouter(prefix="", tags=["ai_ppt"])


def get_ai_ppt_task_progress(
    sid: str,
    client: xunfei_aippt.XunFeiAiPPTClient,
    db: Session,
    max_errors: int = 10  
):
    """
    获取一个AI PPT任务的进度
    """
    error_count = 0
    while True:
        try:
            task_progress = client.get_task_progress(sid)
            crud.update_ai_ppt_record(
                db,
                sid,
                schemas.AiPPTRecordUpdate(
                    process=task_progress.process,
                    err_msg=task_progress.errMsg,
                    ppt_url=task_progress.pptUrl
                )
            )
        except Exception as e:
            logging.error(e)
            error_count += 1
            if error_count >= max_errors:
                logging.error(f"Exceeded maximum number of errors: {max_errors}")
                break
        
        if task_progress.process == 100:
            break
        else:
            time.sleep(20)


class CreateAiPPTTaskRequest(BaseModel):
    text: str

@router.post("/aippt/task", response_model=schemas.AiPPTRecord)
def create_ai_ppt_task(
    request: CreateAiPPTTaskRequest,
    db: Session = Depends(dependencies.get_db),
    current_user: models.User = Depends(dependencies.check_is_expired),
):
    """
    创建一个AI PPT任务
    """
    config = crud.api_config.random_get_enabled_api_config_xunfei_ai_ppt(db)
    if config is None:
        raise HTTPException(
            status_code=404,
            detail=ErrorDetail.from_error_code(ErrorCode.API_CONFIG_NOT_FOUND),
        )
    
    client = xunfei_aippt.XunFeiAiPPTClient(config.app_id, config.api_secret)  # type: ignore
    task_info = client.create_task_from_text(request.text)
    record = crud.create_ai_ppt_record(
        db,
        schemas.AiPPTRecordCreate(
            user_id=current_user.id, # type: ignore
            text = request.text,
            sid = task_info.sid,
            title = task_info.title,
            sub_title = task_info.subTitle,
            cover_img_src = task_info.coverImgSrc,
        ),
        )

    return record

@router.get("/aippt/task/{sid}", response_model=schemas.AiPPTRecord)
def get_ai_ppt_task_by_sid(
    sid: str,
    db: Session = Depends(dependencies.get_db),
    current_user: models.User = Depends(dependencies.check_is_expired),
):
    """
    获取一个AI PPT任务的进度
    """
    record = crud.get_ai_ppt_record_by_sid(db, sid)
    if record is None:
        raise HTTPException(
            status_code=404,
            detail=ErrorDetail.from_error_code(ErrorCode.AI_PPT_TASK_NOT_FOUND),
        )
    return record

@router.get("/aippt/task", response_model=List[schemas.AiPPTRecord])
def get_ai_ppt_by_page(
    page: int = Query(1, ge=1), per_page: int = Query(10, ge=1,le=100),
    db: Session = Depends(dependencies.get_db), current_user: models.User = Depends(dependencies.check_is_expired)):
    return crud.get_ai_ppt_records_by_user_id(db,current_user.id ,page, per_page) # type: ignore
