import logging
from pprint import pprint
import uuid
from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from pydantic import BaseModel
from sqlalchemy.orm import Session
from typing import Dict, List
from app import crud, schemas, models
from app.core import dependencies, utils
from app.schemas import ErrorCode, ErrorDetail
from datetime import timedelta
from app.service.bytedance_openspeech import (
    BytedanceOpenspeechClient,
    BytedanceOpenspeechClientError,
)
from app.core.redis_client import redis_client

router = APIRouter(prefix="", tags=["speech"])

server_ip = utils.get_external_ip()


callback_url = f"http://{server_ip}:8000/api/speech/callback"


class CallbackResponse(BaseModel):
    id: str
    code: int
    message: str
    text: str
    utterances: List[Dict]


class SpeechCallbackRequest(BaseModel):
    resp: CallbackResponse


class SpeechTask(BaseModel):
    status: int
    username: str
    audio_url: str
    text: str = ""


class SpeechTaskUpdate(BaseModel):
    status: int | None = None
    username: str | None = None
    audio_url: str | None = None
    text: str | None = None


@router.post("/speech/callback")
def speech_callback(data: SpeechCallbackRequest):
    task_id = data.resp.id

    if data.resp.code == 1000 and redis_client.task_exists(task_id):
        redis_client.update_task(
            task_id,
            SpeechTaskUpdate(status=1, text=data.resp.text).model_dump(
                exclude_unset=True
            ),
        )

    return {"status": "ok"}


class SpeechSubmitResponse(BaseModel):
    task_id: str
    query_url: str


@router.post("/speech/submit", response_model=SpeechSubmitResponse)
async def speech_submit(
    file: UploadFile = File(...),
    user: models.User = Depends(dependencies.check_is_expired),
    db: Session = Depends(dependencies.get_db),
):
    if file.content_type != "audio/mpeg":
        raise HTTPException(
            status_code=400,
            detail=ErrorDetail.from_error_code(ErrorCode.SPEECH_INVALID_FILE),
        )

    audio_bytes = await file.read()
    unique_filename = f"{uuid.uuid4()}.mp3"
    audio_location = f"./uploaded_files/audios/{unique_filename}"
    with open(audio_location, "wb") as f:
        f.write(audio_bytes)

    audio_url = f"http://{server_ip}:8000/uploaded_files/audios/{unique_filename}"
    speech_client_config = crud.random_get_enabled_api_config_bytedance_openspeech(db)
    if not speech_client_config:
        raise HTTPException(
            status_code=404,
            detail=ErrorDetail.from_error_code(ErrorCode.API_CONFIG_NOT_FOUND),
        )
    speech_client = BytedanceOpenspeechClient(
        appid=speech_client_config.appid,  # type: ignore
        token=speech_client_config.token,  # type: ignore
        cluster=speech_client_config.cluster,  # type: ignore
        callback_url=callback_url,
    )
    try:
        task_id = speech_client.submit(audio_url, user.username)  # type: ignore
        redis_client.set_task(
            task_id,
            SpeechTask(status=0, username=user.username, audio_url=audio_url).model_dump(),  # type: ignore
        )
    except BytedanceOpenspeechClientError as e:
        logging.error(e)
        raise HTTPException(
            status_code=500,
            detail=ErrorDetail.from_error_code(ErrorCode.SPEECH_PROCCESS_ERROR),
        )

    return {
        "task_id": task_id,
        "query_url": f"http://{server_ip}:8000/api/speech/result/{task_id}",
    }


@router.get("/speech/result/{task_id}", response_model=SpeechTask)
def get_task_result(
    task_id: str,
    user: models.User = Depends(dependencies.check_is_expired),
):
    if not redis_client.task_exists(task_id):
        raise HTTPException(
            status_code=404,
            detail=ErrorDetail.from_error_code(ErrorCode.SPEECH_TASK_NOT_FOUND),
        )

    task = redis_client.get_task(task_id)
    return task
