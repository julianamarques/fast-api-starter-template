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
    TOKEN_ALGORITHM: str = "HS256"
    SECRET_KEY: str = Field(min_length=32)
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8
    FRONTEND_URL: str = ""
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
        origins = [str(origin).rstrip("/") for origin in self.BACKEND_CORS_ORIGINS]

        if self.FRONTEND_URL:
            origins.append(self.FRONTEND_URL.rstrip("/"))

        return origins

    @property
    def is_production(self) -> bool:
        return self.ENVIRONMENT == "production"

    @property
    def openapi_url(self) -> str | None:
        return None if self.is_production else f"{self.API_PREFIX}/openapi.json"

    @property
    def docs_url(self) -> str | None:
        return None if self.is_production else "/docs"

    @property
    def redoc_url(self) -> str | None:
        return None if self.is_production else "/redoc"

    PROJECT_NAME: str = "Fast API Starter Template"
    VERSION: str = "0.1.0"
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


settings = Settings()
