import jwt
from datetime import datetime, timedelta
from pydantic import BaseModel
from app.core.config import CONFIG
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
import base64
from typing import Tuple

class TokenData(BaseModel):
    username: str


class Token(BaseModel):
    access_token: str
    token_type: str
    expire_at: datetime


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now() + expires_delta
    else:
        expire = datetime.now() + timedelta(minutes=CONFIG.JWT.EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, CONFIG.JWT.SECRET_KEY, algorithm=CONFIG.JWT.ALGORITHM
    )
    return encoded_jwt


def verify_access_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(
            token, CONFIG.JWT.SECRET_KEY, algorithms=[CONFIG.JWT.ALGORITHM]
        )
        username: str|None = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except jwt.PyJWTError:
        raise credentials_exception
    return token_data



def aes_decrypt(ciphertext:str, key:bytes) -> Tuple[int, str]:
    # 使用冒号分隔 IV 和 密文
    iv_str, encrypted_text_str = ciphertext.split(':')
    # base64 解码
    iv = base64.b64decode(iv_str)
    encrypted_text = base64.b64decode(encrypted_text_str)
    # 创建AES解密器
    cipher = AES.new(key, AES.MODE_CBC, iv)
    # 解密并去填充
    decrypted_data = unpad(cipher.decrypt(encrypted_text), AES.block_size)
    # 提取时间戳和明文
    timestamp, plaintext = decrypted_data.split(b"||", 1)
    return int(timestamp.decode('utf-8')), plaintext.decode('utf-8')