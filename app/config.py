from typing import List

from aiogram.types import BotCommand
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Настройки приложения."""

    TOKEN: str
    SQLITE_BASE: str
    MUSIC_PATH: str  # Путь для скачивания музыки из музыкального архива
    UPLOAD_PATH_MUSIC_ACRHIVE: str # Путь где хранится json файл с именами и жанрами исполнителей
    # из музыкального архива
    HITMOTOP_SEARCH_URL: str = (
        "https://ru.hitmotop.com/search?q="  # путь для поиска музыки с сайта hitmotop
    )
    HITMOTOP_PATH: str = "media\hitmotop" # путь для хранения скаченой музыки с сайта hitmitop
    COUNT_HITMOTOP: int = 30  # количество песеня для скачивания с сайта hitmotop
    AlBUM_TITLE_COLLECTION: str = "Сборник песен"  # Название для сборника пользователя
    MUSIC_FORMAT_LIST: List = ["mp3", "wav", "m4a", "ogg", "flac"]
    IMG_FORMAT_LIST: List = ["jpg", "jpeg", "gif", "png", "bmp"]
    bot_command: List = [
        BotCommand(
            command="/start",
            description="Меню бота",
        ),
        BotCommand(
            command="/admin",
            description="Для администраторов",
        ),
        BotCommand(
            command="/help",
            description="Описание умений бота",
        ),
    ]
    ADMINS_LIST: List[int] = []

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
