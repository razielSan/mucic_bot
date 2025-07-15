from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram.types.keyboard_button import KeyboardButton


def get_music_menu_button():
    """Возвращает кнопки главного меню бота."""
    reply_kb = ReplyKeyboardBuilder(
        [
            [KeyboardButton(text="Добавить музыку")],
        ]
    )

    return reply_kb.as_markup(resize_keyboard=True)
