from typing import List

from aiogram.types import BotCommand

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Настройка приложения."""

    TOKEN: str
    SQLITE_BASE: str
    TOKEN_VK: str
    CLIENT_ID: str
    CLIENT_SECRET: str
    MUSIC_PATH: str
    bot_command: List = [
        BotCommand(
            command="/start",
            description="Меню бота",
        ),
        BotCommand(
            command="/help",
            description="Описание умений бота",
        ),
    ]

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
