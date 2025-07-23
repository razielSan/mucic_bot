from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import CommandStart

from extensions import bot
from keyboards.reply import get_music_menu_button
from repository.genreExecutor import GenreExecutorSQLAlchemyRepository


router = Router()


@router.message(CommandStart())
async def start(message: Message):
    """Возвращает главное меню бота."""
    chat_id = message.chat.id
    message_id = message.message_id

    await bot.delete_message(chat_id=chat_id, message_id=message_id)
    await message.answer(
        text="Музыкальный архив",
        reply_markup=get_music_menu_button(),
    )
