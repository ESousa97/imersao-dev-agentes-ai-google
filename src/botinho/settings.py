"""Application settings loaded from environment variables."""

from __future__ import annotations

from functools import lru_cache

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    app_name: str = "Botinho - Chat AI"
    app_version: str = "2.1.0"
    environment: str = Field(default="development", alias="BOTINHO_ENV")
    host: str = Field(default="0.0.0.0", alias="BOTINHO_HOST")
    port: int = Field(default=8000, alias="BOTINHO_PORT")
    log_level: str = Field(default="INFO", alias="BOTINHO_LOG_LEVEL")

    gemini_api_key: str = Field(default="", alias="GEMINI_API_KEY")
    gemini_model: str = Field(default="gemini-2.0-flash", alias="BOTINHO_GEMINI_MODEL")

    cors_allowed_origins: list[str] = Field(
        default_factory=lambda: ["http://localhost:8000", "http://127.0.0.1:8000"],
        alias="BOTINHO_CORS_ALLOWED_ORIGINS",
    )

    rate_limit_requests: int = Field(default=60, alias="BOTINHO_RATE_LIMIT_REQUESTS")
    rate_limit_window_seconds: int = Field(default=60, alias="BOTINHO_RATE_LIMIT_WINDOW_SECONDS")

    @field_validator("cors_allowed_origins", mode="before")
    @classmethod
    def _parse_cors_allowed_origins(cls, value: str | list[str]) -> list[str]:
        if isinstance(value, list):
            return value
        if isinstance(value, str):
            return [entry.strip() for entry in value.split(",") if entry.strip()]
        return ["http://localhost:8000", "http://127.0.0.1:8000"]

    @field_validator("gemini_model", mode="before")
    @classmethod
    def _normalize_gemini_model(cls, value: str) -> str:
        if not isinstance(value, str):
            return "gemini-2.0-flash"

        normalized = value.strip().lower()
        if not normalized:
            return "gemini-2.0-flash"

        normalized = normalized.replace("lastest", "latest")
        return normalized


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()
