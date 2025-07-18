from typing import List

from aiogram.types import BotCommand

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Настройка приложения."""

    TOKEN: str
    SQLITE_BASE: str
    bot_command: List = [
        BotCommand(
            command="/start",
            description="Меню бота",
        ),
    ]

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
