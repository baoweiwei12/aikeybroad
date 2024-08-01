import logging
import uuid
import bcrypt
import requests
from sqlalchemy.orm import Session
from app import models


def hash_password(password: str) -> str:
    """Hash a password for storing."""
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode("utf-8"), salt)
    return hashed.decode("utf-8")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a stored password against one provided by user."""
    return bcrypt.checkpw(
        plain_password.encode("utf-8"), hashed_password.encode("utf-8")
    )


def generate_unique_cdkey(db: Session) -> str:
    """生成唯一的 xxxx-xxxx-xxxx-xxxx 格式的 CDKey"""
    while True:
        # 生成一个随机的 UUID 并格式化为 xxxx-xxxx-xxxx-xxxx
        uuid_str = str(uuid.uuid4()).replace("-", "")[:16]
        cdkey = f"{uuid_str[:4]}-{uuid_str[4:8]}-{uuid_str[8:12]}-{uuid_str[12:16]}"

        # 检查数据库中是否已存在相同的 CDKey
        existing_cdkey = (
            db.query(models.Cdkey).filter(models.Cdkey.key == cdkey).first()
        )
        if not existing_cdkey:
            return cdkey


def get_external_ip():
    try:
        response = requests.get("https://ipinfo.io/json")
        response.raise_for_status()

        ip = response.json().get("ip")
        return ip
    except requests.RequestException as e:
        logging.error(f"An error occurred: {e}")
        return None
