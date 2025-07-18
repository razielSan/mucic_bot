from aiogram import Router, F
from aiogram.types import CallbackQuery, Message

from repository.executor import ExecutorSQLAlchemyRepository
from repository.album import AlbumSQLAlchemyRepository
from repository.genre import GengreSQLAlchemyRepository
from repository.song import SongSQLAlchemyRepository
from repository.user import UserSQLAlchemyRepository


router = Router(name=__name__)


@router.message(F.text == "Список исполниетелей")
async def get_list_executors(message: Message):
    pass