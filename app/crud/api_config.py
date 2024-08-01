from datetime import datetime, timedelta
import logging
from typing import List
from sqlalchemy import func, select, insert, update, delete
from sqlalchemy.orm import Session
from app import schemas, models
from app.core import utils
from app.core.database import SessionLocal


def create_api_config_doubao_glm(
    db: Session, api_config: schemas.ApiConfigDouBaoGLMCreate
):
    db_api_config = models.ApiConfigDouBaoGLM(**api_config.model_dump())
    db.add(db_api_config)
    db.commit()
    db.refresh(db_api_config)
    return db_api_config


def create_api_config_xunfei_ai_ppt(
    db: Session, api_config: schemas.ApiConfigXunFeiAiPPTCreate
):
    db_api_config = models.ApiConfigXunFeiAiPPT(**api_config.model_dump())
    db.add(db_api_config)
    db.commit()
    db.refresh(db_api_config)
    return db_api_config


def get_api_config_doubao_glm(db: Session, api_config_id: int):
    return (
        db.query(models.ApiConfigDouBaoGLM)
        .filter(models.ApiConfigDouBaoGLM.id == api_config_id)
        .first()
    )


def get_api_config_doubao_glm_by_page(db: Session, page: int = 1, per_page: int = 10):
    return (
        db.query(models.ApiConfigDouBaoGLM)
        .offset((page - 1) * per_page)
        .limit(per_page)
        .all()
    )


def random_get_enabled_api_config_doubao_glm(db: Session):
    return (
        db.query(models.ApiConfigDouBaoGLM)
        .filter(models.ApiConfigDouBaoGLM.enabled == True)
        .order_by(func.random())
        .first()
    )


def get_api_config_xunfei_ai_ppt(db: Session, api_config_id: int):
    return (
        db.query(models.ApiConfigXunFeiAiPPT)
        .filter(models.ApiConfigXunFeiAiPPT.id == api_config_id)
        .first()
    )


def get_api_config_xunfei_ai_ppt_by_page(
    db: Session, page: int = 1, per_page: int = 10
):
    return (
        db.query(models.ApiConfigXunFeiAiPPT)
        .offset((page - 1) * per_page)
        .limit(per_page)
        .all()
    )


def random_get_enabled_api_config_xunfei_ai_ppt(db: Session):
    return (
        db.query(models.ApiConfigXunFeiAiPPT)
        .filter(models.ApiConfigXunFeiAiPPT.enabled == True)
        .order_by(func.random())
        .first()
    )


def update_api_config_doubao_glm(
    db: Session, api_config_id: int, api_config: schemas.ApiConfigDouBaoGLMUpdate
):
    db_api_config = (
        db.query(models.ApiConfigDouBaoGLM)
        .filter(models.ApiConfigDouBaoGLM.id == api_config_id)
        .first()
    )
    if not db_api_config:
        return None
    update_data = api_config.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_api_config, key, value)
    db.commit()
    db.refresh(db_api_config)
    return db_api_config


def update_api_config_xunfei_ai_ppt(
    db: Session, api_config_id: int, api_config: schemas.ApiConfigXunFeiAiPPTUpdate
):
    db_api_config = (
        db.query(models.ApiConfigXunFeiAiPPT)
        .filter(models.ApiConfigXunFeiAiPPT.id == api_config_id)
        .first()
    )
    if not db_api_config:
        return None
    update_data = api_config.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_api_config, key, value)
    db.commit()
    db.refresh(db_api_config)
    return db_api_config


def get_api_config_bytedance_openspeech(db: Session, api_config_id: int):

    return (
        db.execute(
            select(models.ApiConfigBytedanceOpenspeech).where(
                models.ApiConfigBytedanceOpenspeech.id == api_config_id
            )
        )
        .scalars()
        .first()
    )


def get_api_config_bytedance_openspeech_by_page(
    db: Session, page: int = 1, per_page: int = 10
):
    return (
        db.execute(
            select(models.ApiConfigBytedanceOpenspeech)
            .offset((page - 1) * per_page)
            .limit(per_page)
        )
        .scalars()
        .all()
    )


def random_get_enabled_api_config_bytedance_openspeech(db: Session):
    return (
        db.execute(
            select(models.ApiConfigBytedanceOpenspeech)
            .where(models.ApiConfigBytedanceOpenspeech.enabled == True)
            .order_by(func.random())
        )
        .scalars()
        .first()
    )


def create_api_config_bytedance_openspeech(
    db: Session, api_config: schemas.ApiConfigByteDanceOpenspeechCreate
):

    db_api_config = models.ApiConfigBytedanceOpenspeech(**api_config.model_dump())
    db.add(db_api_config)
    db.commit()
    db.refresh(db_api_config)
    return db_api_config


def update_api_config_bytedance_openspeech(
    db: Session,
    api_config_id: int,
    api_config: schemas.ApiConfigByteDanceOpenspeechUpdate,
):
    db_api_config = (
        db.query(models.ApiConfigBytedanceOpenspeech)
        .filter(models.ApiConfigBytedanceOpenspeech.id == api_config_id)
        .first()
    )
    if not db_api_config:
        return None
    update_data = api_config.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_api_config, key, value)
    db.commit()
    db.refresh(db_api_config)
    return db_api_config
