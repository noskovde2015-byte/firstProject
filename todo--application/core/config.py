from pathlib import Path

from pydantic import BaseModel, PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict


class RunConfig(BaseModel):
    port: int = 8002
    host: str = "127.0.0.1"


class ApiV1Prefix(BaseModel):
    prefix: str = "/v1"
    user: str = "/user"
    reg: str = "/register"
    log: str = "/login"


class ApiPrefix(BaseModel):
    prefix: str = "/api"
    v1: ApiV1Prefix = ApiV1Prefix()


class DataBaseConfig(BaseModel):
    url: PostgresDsn
    echo: bool = False
    echo_pool: bool = False
    max_overflow: int = 10
    pool_size: int = 50


class Auth(BaseModel):
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE: int

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=Path(__file__).parent.parent / ".env",
        case_sensitive=False,
        env_file_encoding="utf-8",
        env_prefix="APP_CONFIG__",
        env_nested_delimiter="__"
    )

    run: RunConfig = RunConfig()
    api: ApiPrefix = ApiPrefix()
    db: DataBaseConfig
    auth: Auth


settings = Settings()

