from aiogram import Router, F
from aiogram.types import Message, ReplyKeyboardRemove
from extensions import bot

from filters import IsAdmin
from keyboards.reply import get_menu_admin
from functions import create_json_executors_dict
from config import settings


router = Router(
    name=__name__,
)


@router.message(IsAdmin(), F.text == "/admin")
async def admin_handler(message: Message):
    """Возвращает кнопки меню администратора."""
    await message.answer(
        f"Привет, {message.from_user.first_name}",
        reply_markup=ReplyKeyboardRemove(),
    )
    await bot.send_message(
        chat_id=message.chat.id,
        text="Меню администратора",
        reply_markup=get_menu_admin(),
    )


@router.message(
    IsAdmin(),
    F.text == "Обновить список исполнителей для музыкального хранилища",
)
async def update_music_archive(message: Message):
    """Обновляет список исполнителей для музыкального хранилища."""
    result: bool = create_json_executors_dict(
        path=settings.MUSIC_PATH,
        upload_path=settings.UPLOAD_PATH_MUSIC_ACRHIVE,
    )

    await bot.send_message(
        chat_id=message.chat.id,
        text="Идет обновление списка",
    )
    if result:
        await message.answer(
            "Список успешно обновлен",
            reply_markup=get_menu_admin(),
        )
    else:
        await message.answer(
            "Произошла ошибка при обновлении",
            reply_markup=get_menu_admin(),
        )
