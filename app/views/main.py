from aiogram import Router, F
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.types.input_file import FSInputFile
from aiogram.filters import CommandStart

from extensions import bot
from keyboards.reply import get_music_menu_button
from functions import get_info_is_bot


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


@router.message(F.text == "/help")
async def help(message: Message):
    """Возвращает описание умения бота."""
    await message.answer(
        text=get_info_is_bot(),
        reply_markup=ReplyKeyboardRemove(),
    )


@router.message(F.text == "q")
async def help(message: Message):
    """Возвращает описание умения бота."""
    path = "D:\Media\Music\Анархо\Анархо-шансон\Катя Беломоркина (Петрозаводск)\(666)-Сборник песен\Народовольческая.mp3"
    await message.answer_audio(audio=FSInputFile(path=path))