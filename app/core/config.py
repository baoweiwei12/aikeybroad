from typing import Any, Dict
from pydantic import BaseModel
import yaml


class MYSQLSettings(BaseModel):
    HOST: str
    PORT: int
    USER: str
    PASSWORD: str
    DATABASE: str


class JWTSettings(BaseModel):
    SECRET_KEY: str
    ALGORITHM: str
    EXPIRE_MINUTES: int


class AppSettings(BaseModel):
    NAME: str
    VERSION: str
    DESCRIPTION: str


class AppConfig(BaseModel):
    APP: AppSettings
    MYSQL: MYSQLSettings
    JWT: JWTSettings

    @classmethod
    def from_yaml(cls, file_path: str):
        with open(file_path, "r") as file:
            config_data: Dict[str, Any] = yaml.safe_load(file)
        return cls(**config_data)


CONFIG = AppConfig.from_yaml("config.yaml")
