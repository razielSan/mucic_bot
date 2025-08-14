from aiogram.filters import Filter
from aiogram.types import Message

from config import settings


class IsAdmin(Filter):
    def __init__(self) -> None:
        pass

    async def __call__(self, message: Message):
        return message.chat.id in settings.ADMINS_LIST
