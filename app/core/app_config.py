import os
from typing import Any, Literal, Annotated

from pydantic import BeforeValidator, AnyUrl, Field
from pydantic_core import MultiHostUrl
from pydantic_settings import BaseSettings, SettingsConfigDict


def parse_cors(v: Any) -> list[str] | str:
    if isinstance(v, str) and not v.startswith("["):
        return [i.strip() for i in v.split(",")]
    elif isinstance(v, list | str):
        return v
    raise ValueError(v)


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=os.path.join(os.path.dirname(__file__), "../../.env"),
        env_ignore_empty=True,
        extra="ignore"
    )

    API_PREFIX: str = ""
    TOKEN_ALGORITHM: str = ""
    SECRET_KEY: str = ""
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8
    FRONTEND_URL: str = "http://localhost:4200"
    ENVIRONMENT: Literal[
        "production",
        "development",
        "testing"
    ] = "development"
    BACKEND_CORS_ORIGINS: Annotated[
        list[AnyUrl] | str, BeforeValidator(parse_cors)
    ] = Field(default_factory=list)

    @property
    def all_cors_origins(self) -> list[str]:
        return [str(origin).rstrip("/") for origin in self.BACKEND_CORS_ORIGINS] + [self.FRONTEND_URL]

    PROJECT_NAME: str = ""
    VERSION: str = ""
    POSTGRES_SERVER: str = ""
    POSTGRES_PORT: int = 5432
    POSTGRES_USER: str = ""
    POSTGRES_PASSWORD: str = ""
    POSTGRES_DATABASE: str = ""
    POSTGRES_SCHEME: str = ""

    @property
    def get_sqlalchemy_database_uri(self) -> MultiHostUrl:
        return MultiHostUrl.build(
            scheme=self.POSTGRES_SCHEME,
            username=self.POSTGRES_USER,
            password=self.POSTGRES_PASSWORD,
            host=self.POSTGRES_SERVER,
            port=self.POSTGRES_PORT,
            path=self.POSTGRES_DATABASE,
        )

    ADMIN_USER: str = ""
    ADMIN_PASSWORD: str = ""


settings = Settings()
