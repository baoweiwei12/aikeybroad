from pydantic import BaseModel

from enum import Enum


class ErrorCode(Enum):
    PASSWORD_INCORRECT = (1001, "密码错误")
    ACCOUNT_NOT_FOUND = (1002, "账号不存在")
    PERMISSION_DENIED = (1003, "权限不足")
    TOKEN_EXPIRED = (1004, "token已过期")
    ACCOUNT_ALREADY_EXISTS = (1005, "账号已存在")
    TOKEN_VALIDATION_ERROR = (1006, "令牌验证失败")
    ACCOUNT_DISABLED = (1007, "账号已禁用")
    EMAIL_ALREADY_EXISTS = (1008, "邮箱已存在")
    USERNAME_ALREADY_EXISTS = (1009, "用户名已存在")
    USER_NOT_FOUND = (1010, "用户不存在")
    PASSWORD_NOT_MATCH = (1011, "两次密码不匹配")
    IS_EXPIRED = (1012, "使用权限已过期")

    CDKEY_NOT_FOUND = (2001, "CDKEY不存在")
    CDKEY_USED = (2002, "CDKEY已使用")
    CDKEY_EXPIRED = (2003, "CDKEY已过期")

    def __init__(self, code, message):
        self.code = code
        self.message = message


class ErrorDetail(BaseModel):
    error: str
    code: int
    message: str

    @classmethod
    def from_error_code(cls, error_code: ErrorCode):
        return cls(
            error=error_code.name,
            code=error_code.code,
            message=error_code.message,
        ).model_dump()
