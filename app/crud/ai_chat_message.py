from datetime import datetime, timedelta
import logging
from typing import List
from sqlalchemy import desc, func, select, insert, update, delete
from sqlalchemy.orm import Session
from app import schemas, models
from app.core import utils


def create_ai_chat_message(
    db: Session,
    new_ai_chat_message:schemas.AiChatMessageCreate
) :
    db_chat_message = models.AiChatMessage(**new_ai_chat_message.model_dump())

    db.add(db_chat_message)
    db.commit()
    db.refresh(db_chat_message)
    return db_chat_message

def get_ai_chat_message_by_user_id(
    db: Session,
    user_id: int,
    offset: int
) :
    return (
        db.query(models.AiChatMessage)
        .filter(models.AiChatMessage.user_id == user_id)
        .order_by(desc(models.AiChatMessage.id))
        .offset(offset)
        .first()
    )