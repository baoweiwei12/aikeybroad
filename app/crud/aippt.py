from datetime import datetime, timedelta
import logging
from typing import List
from sqlalchemy import desc, func, select, insert, update, delete
from sqlalchemy.orm import Session
from app import schemas, models
from app.core import utils


def get_ai_ppt_record_by_sid(db: Session, sid: str):
    return db.query(models.AiPPTRecord).filter(models.AiPPTRecord.sid == sid).first()


def get_ai_ppt_records_by_user_id(db: Session, user_id: int, page: int, per_page: int):
    return (
        db.query(models.AiPPTRecord)
        .filter(models.AiPPTRecord.user_id == user_id)
        .order_by(desc(models.AiPPTRecord.id))
        .offset((page - 1) * per_page)
        .limit(per_page)
        .all()
    )


def create_ai_ppt_record(db: Session, record: schemas.AiPPTRecordCreate):
    db_record = models.AiPPTRecord(**record.model_dump())
    db.add(db_record)
    db.commit()
    db.refresh(db_record)
    return db_record


def update_ai_ppt_record(db: Session, sid: str, record: schemas.AiPPTRecordUpdate):
    db_record = (
        db.query(models.AiPPTRecord).filter(models.AiPPTRecord.sid == sid).first()
    )
    if db_record is None:
        return None
    for key, value in record.model_dump(exclude_unset=True).items():
        setattr(db_record, key, value)
    db.commit()
    db.refresh(db_record)
    return db_record


def get_unfinished_ai_ppt_record(db: Session, max_errors: int = 10):
    return (
        db.query(models.AiPPTRecord)
        .filter(
            models.AiPPTRecord.process != 100,
            models.AiPPTRecord.error_count <= max_errors,
        )
        .first()
    )
