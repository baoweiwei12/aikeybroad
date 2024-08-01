from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel
from sqlalchemy.orm import Session
from typing import List, Literal, Required, TypedDict, Union, Sequence
from app import crud, schemas, models
from app.core import dependencies, utils
from app.schemas import ErrorCode, ErrorDetail
from datetime import timedelta
from app.service import doubao_glm
from volcenginesdkarkruntime.types.chat import (
    ChatCompletion,
)
from volcenginesdkarkruntime.types.chat.chat_completion_system_message_param import (
    ChatCompletionSystemMessageParam,
)

router = APIRouter(prefix="", tags=["aichat"])


class UserMessageParam(TypedDict, total=False):
    content: Required[str]
    role: Required[Literal["user"]]


class AssistantMessageParam(TypedDict, total=False):
    content: Required[str]
    role: Required[Literal["assistant"]]


class ChatRequest(BaseModel):
    messages: List[UserMessageParam | AssistantMessageParam]


@router.post("/aichat", response_model=ChatCompletion)
def chat(
    request: ChatRequest,
    db: Session = Depends(dependencies.get_db),
    current_user: models.User = Depends(dependencies.check_is_expired),
):
    system_message: ChatCompletionSystemMessageParam = {
        "role": "system",
        "content": "你是一个AI键盘精灵,名字叫多多,你乐于助人。",
    }
    messages = [system_message] + request.messages
    random_doubao_config = crud.api_config.random_get_enabled_api_config_doubao_glm(db)

    if random_doubao_config is None:
        raise HTTPException(
            status_code=404,
            detail=ErrorDetail.from_error_code(ErrorCode.API_CONFIG_NOT_FOUND),
        )
    glm = doubao_glm.DouBaoGLM(random_doubao_config.api_key, random_doubao_config.model)  # type: ignore

    completion = glm.chat(messages)  # type: ignore
    return completion
