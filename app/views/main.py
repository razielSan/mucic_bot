from aiogram import Router, F
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.filters import CommandStart

from extensions import bot
from keyboards.reply import get_music_menu_button
from functions import get_info_is_bot
from repository.user import UserSQLAlchemyRepository


router = Router()


@router.message(CommandStart())
async def start(message: Message):
    """Возвращает главное меню бота."""
    chat_id = message.chat.id
    message_id = message.message_id

    user = UserSQLAlchemyRepository().get_user_by_telegram(
        telegram=message.chat.id,
    )
    if not user:
        UserSQLAlchemyRepository().create_user(
            telegram=message.chat.id,
            name=message.from_user.first_name,
        )

    await bot.delete_message(chat_id=chat_id, message_id=message_id)
    await message.answer(
        text="Музыкальный архив",
        reply_markup=get_music_menu_button(),
    )


@router.message(F.text == "/help")
async def help(message: Message):
    """Возвращает описание умения бота."""
    await message.answer(
        text=get_info_is_bot(),
        reply_markup=ReplyKeyboardRemove(),
    )
