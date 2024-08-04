import logging
from pprint import pprint
from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel
from sqlalchemy.orm import Session
from typing import List, Literal, Required, TypedDict, Union, Sequence
from app import crud, schemas, models
from app.core import dependencies, utils
from app.schemas import ErrorCode, ErrorDetail
from datetime import timedelta
from app.service import doubao_glm, glm_token
from volcenginesdkarkruntime.types.chat import (
    ChatCompletion,
)

from volcenginesdkarkruntime.types.chat.chat_completion_tool_message_param import (
    ChatCompletionToolMessageParam,
)
from volcenginesdkarkruntime.types.chat.chat_completion_user_message_param import (
    ChatCompletionUserMessageParam,
)
from volcenginesdkarkruntime.types.chat.chat_completion_system_message_param import (
    ChatCompletionSystemMessageParam,
)
from volcenginesdkarkruntime.types.chat.chat_completion_function_message_param import (
    ChatCompletionFunctionMessageParam,
)
from volcenginesdkarkruntime.types.chat.chat_completion_assistant_message_param import (
    ChatCompletionAssistantMessageParam,
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


@router.post("/chat/completion", response_model=ChatCompletion)
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


class ChatNextRequest(BaseModel):
    content: str


class ChatNextResponse(BaseModel):
    content: str


@router.post("/chat/next", response_model=ChatNextResponse)
def chat_next(
    request: ChatNextRequest,
    db: Session = Depends(dependencies.get_db),
    current_user: models.User = Depends(dependencies.check_is_expired),
):
    random_doubao_config = crud.api_config.random_get_enabled_api_config_doubao_glm(db)
    if random_doubao_config is None:
        raise HTTPException(
            status_code=404,
            detail=ErrorDetail.from_error_code(ErrorCode.API_CONFIG_NOT_FOUND),
        )

    glm = doubao_glm.DouBaoGLM(random_doubao_config.api_key, random_doubao_config.model)  # type: ignore
    messages = [
        {
            "role": "system",
            "content": "你是一个AI键盘精灵,名字叫多多,你乐于助人。",
        },
        {
            "role": "user",
            "content": request.content,
        },
    ]
    offset = 0
    while True:

        
        chat_message = crud.get_ai_chat_message_by_user_id(db, current_user.id, offset)  # type: ignore
        if chat_message is None:
            break
        messages.insert(1,{"role":chat_message.role,"content":chat_message.content}) # type: ignore
        if glm_token.num_tokens_from_messages(messages) > 28000:
            messages.pop(1)
            break
        offset = offset + 1
    try:
        completion = glm.chat(messages)  # type: ignore
    except Exception as e:
        logging.error(f"chart next error:{e}")
        return ChatNextResponse(content="哎呀！出错了。")
    if (assistant_content := completion.choices[0].message.content) is not None:
        crud.create_ai_chat_message(db, schemas.AiChatMessageCreate(content=request.content, role="user", user_id=current_user.id)) # type: ignore
        crud.create_ai_chat_message(db, schemas.AiChatMessageCreate(content=assistant_content, role="assistant", user_id=current_user.id)) # type: ignore
        return ChatNextResponse(content=assistant_content)
    else:
        return ChatNextResponse(content="哎呀！出错了。")
