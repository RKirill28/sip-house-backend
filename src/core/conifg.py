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
    done_projects_prefix: str = "/done_projects"
    images_prefix: str = "/images"
    files_prefix: str = "/files"
    auth_prefix: str = "/auth"


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

    token_secret: str = "h+eCFlT=mF%Q(!36~W5~n8;=[sY#17[&hQ]ejeuICR5LLHRK17"
    admin_username: str = "admin"
    admin_pass: str = "admin1234"
    ACCESS_TOKEN_MAX_AGE_IN_MINUTES: int = 1440

    BASE_DIR: Path = Path(__file__).resolve().parent.parent.parent.parent
    UPLOADS_BASE_DIR: Path = BASE_DIR / "uploads"
    IMAGE_MAX_WIDTH: int = 600


settings = Settings()
