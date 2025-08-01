from typing import List

from aiogram.types import BotCommand
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Настройка приложения."""

    TOKEN: str
    SQLITE_BASE: str
    MUSIC_PATH: str # Путь для скачивания музыки по сети 
    AlBUM_TITLE_COLLECTION: str = "Сборник песен" # Название для сборника пользователя
    MUSIC_FORMAT_LIST: List = ["mp3", "wav", "m4a", "ogg", "flac"]
    IMG_FORMAT_LIST: List = ["jpg", "jpeg", "gif", "png", "bmp"]
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
