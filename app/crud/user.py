from datetime import datetime, timedelta
import logging
from typing import List
from sqlalchemy.orm import Session
from sqlalchemy import delete, select, insert, update
from app import schemas, models
from app.core import utils
from app.core.database import SessionLocal


def get_user(db: Session, user_id: int) -> models.User | None:
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_username(db: Session, username: str) -> models.User | None:
    return db.query(models.User).filter(models.User.username == username).first()


def get_user_by_email(db: Session, email: str) -> models.User | None:
    return db.query(models.User).filter(models.User.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 10) -> List[models.User] | None:
    return db.query(models.User).offset(skip).limit(limit).all()


def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = utils.hash_password(user.password)
    db_user = models.User(
        username=user.username,
        email=user.email,
        hashed_password=hashed_password,
        full_name=user.full_name,
        disabled=user.disabled,
        role=user.role,
        expiration_date=user.expiration_date,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def update_user(db: Session, user_id: int, user_update: schemas.UserUpdate):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if db_user is None:
        return None
    update_data = user_update.model_dump(exclude_unset=True)
    if "password" in update_data:
        update_data["hashed_password"] = utils.hash_password(update_data["password"])
        del update_data["password"]
    for key, value in update_data.items():
        setattr(db_user, key, value)
    db.commit()
    db.refresh(db_user)
    return db_user


def delete_user(db: Session, user_id: int):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if db_user is None:
        return None
    db.delete(db_user)
    db.commit()
    return db_user


# def delete_user(db: Session, user_id: int):
#     query_stmt = select(models.User).where(models.User.id == user_id)
#     db_user = db.execute(query_stmt).scalars().first()
#     if db_user is None:
#         return None
#     delete_stmt = delete(models.User).where(models.User.id == user_id)
#     db.execute(delete_stmt)
#     db.commit()
#     return db_user
def authenticate_user(db: Session, username: str, password: str) -> models.User | None:
    user = get_user_by_username(db, username)
    if user and utils.verify_password(password, str(user.hashed_password)):
        return user
    return None


def init_user():
    try:
        db = SessionLocal()
        admin_user = get_user_by_username(db, "admin")
        if admin_user is None:
            logging.info(f"Added admin user to database")
            admin_user = create_user(
                db,
                schemas.UserCreate(
                    username="admin",
                    email="admin@example.com",
                    password="admin",
                    full_name="超级管理员",
                    role=schemas.RoleOpthons.superadmin,
                    expiration_date=datetime.now() + timedelta(days=365),
                ),
            )

    except Exception as e:
        logging.error(f"Failed to add admin user to database: {e}")
    finally:
        db.close()
