from pathlib import Path
from typing import ClassVar

from pydantic import BaseModel, MySQLDsn
from pydantic_settings import BaseSettings, SettingsConfigDict


class DatabaseConfig(BaseModel):
    async_url: MySQLDsn
    sync_url: MySQLDsn

    echo: bool
    echo_pool: bool


class RunConfig(BaseModel):
    host: str = "0.0.0.0"
    port: int = 8000


class ApiV1PrefixConfig(BaseModel):
    prefix: str = "/v1"
    projects_prefix: str = "/projects"
    images_prefix: str = "/images"


class ApiPrefixConfig(BaseModel):
    api_prefix: str = "/api"
    v1: ApiV1PrefixConfig = ApiV1PrefixConfig()


class Settings(BaseSettings):
    model_config: ClassVar = SettingsConfigDict(
        env_file=(".env.template", ".env"),
        case_sensitive=False,
        env_nested_delimiter="__",
    )

    run: RunConfig = RunConfig()
    api: ApiPrefixConfig = ApiPrefixConfig()
    db: DatabaseConfig
    BASE_DIR: Path = Path(__file__).resolve().parent.parent.parent
    UPLOADS_BASE_DIR: Path = BASE_DIR / "uploads"


settings = Settings()
