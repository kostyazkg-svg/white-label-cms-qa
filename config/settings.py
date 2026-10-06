"""Конфигурация проекта через переменные окружения."""

from pydantic import Field, HttpUrl
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Настройки тестового окружения."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    base_url: HttpUrl = Field(
        default="https://white-label-cms-kostya61371.amvera.io",
        description="Базовый URL тестируемого сайта",
    )
    browser: str = Field(default="chromium")
    headless: bool = Field(default=True)
    default_timeout_ms: int = Field(default=15_000)
    navigation_timeout_ms: int = Field(default=30_000)
    mobile_viewport_width: int = Field(default=375)
    mobile_viewport_height: int = Field(default=812)
    desktop_viewport_width: int = Field(default=1440)
    desktop_viewport_height: int = Field(default=900)


settings = Settings()
