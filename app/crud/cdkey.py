from datetime import datetime, timedelta
import logging
from typing import List
from sqlalchemy.orm import Session
from app import schemas, models
from app.core import utils
from app.core.database import SessionLocal


def get_cdkeys(db: Session, page: int = 1, per_page: int = 10):
    query = db.query(models.Cdkey)
    total = query.count()
    cdkeys = query.offset((page - 1) * per_page).limit(per_page).all()
    return (total, cdkeys)


def get_cdkey(db: Session, cdkey_id: int) -> models.Cdkey | None:
    return db.query(models.Cdkey).filter(models.Cdkey.id == cdkey_id).first()


def create_cdkey(db: Session, cdkey: schemas.CdkeyCreate) -> models.Cdkey:
    db_cdkey = models.Cdkey(**cdkey.model_dump())
    db.add(db_cdkey)
    db.commit()
    db.refresh(db_cdkey)
    return db_cdkey


def create_cdkeys(db: Session, cdkeys: List[schemas.CdkeyCreate]) -> List[models.Cdkey]:
    db_cdkeys = [models.Cdkey(**cdkey.model_dump()) for cdkey in cdkeys]
    db.add_all(db_cdkeys)
    db.commit()
    for db_cdkey in db_cdkeys:
        db.refresh(db_cdkey)
    return db_cdkeys


def update_cdkey(
    db: Session, cdkey_id: int, cdkey: schemas.CdkeyUpdate
) -> models.Cdkey | None:
    db_cdkey = db.query(models.Cdkey).filter(models.Cdkey.id == cdkey_id).first()
    if db_cdkey is None:
        return None
    for key, value in cdkey.model_dump(exclude_unset=True).items():
        setattr(db_cdkey, key, value)
    db.commit()
    db.refresh(db_cdkey)
    return db_cdkey


def delete_cdkey(db: Session, cdkey_id: int) -> models.Cdkey | None:
    db_cdkey = db.query(models.Cdkey).filter(models.Cdkey.id == cdkey_id).first()
    if db_cdkey is None:
        return None
    db.delete(db_cdkey)
    db.commit()
    return db_cdkey


def get_cdkey_by_key(db: Session, key: str):
    return db.query(models.Cdkey).filter(models.Cdkey.key == key).first()
