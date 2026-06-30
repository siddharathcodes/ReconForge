from functools import lru_cache

from pydantic import AnyHttpUrl, Field, PostgresDsn, RedisDsn, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    project_name: str = "ReconForge"
    environment: str = Field(default="development")
    api_version: str = "0.1.0"
    api_prefix: str = "/api/v1"
    debug: bool = False
    enable_docs: bool = True
    log_level: str = "INFO"

    database_url: PostgresDsn = Field(
        default="postgresql+psycopg://reconforge:reconforge@postgres:5432/reconforge"
    )
    database_pool_size: int = 10
    database_max_overflow: int = 20
    database_pool_timeout: int = 30

    redis_url: RedisDsn = Field(default="redis://redis:6379/0")
    celery_broker_url: RedisDsn = Field(default="redis://redis:6379/1")
    celery_result_backend: RedisDsn = Field(default="redis://redis:6379/2")

    cors_origins: list[str] = Field(default_factory=lambda: ["http://localhost:5173"])

    @field_validator("cors_origins", mode="before")
    @classmethod
    def parse_cors_origins(cls, value: str | list[str]) -> list[str]:
        if isinstance(value, str):
            return [origin.strip() for origin in value.split(",") if origin.strip()]
        return value

    @field_validator("log_level")
    @classmethod
    def normalize_log_level(cls, value: str) -> str:
        return value.upper()

    @property
    def frontend_origin(self) -> AnyHttpUrl | None:
        if not self.cors_origins:
            return None
        return AnyHttpUrl(self.cors_origins[0])


@lru_cache
def get_settings() -> Settings:
    return Settings()
