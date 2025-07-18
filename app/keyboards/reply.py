from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram.types.keyboard_button import KeyboardButton


def get_music_menu_button():
    """Возвращает кнопки главного меню бота."""
    reply_kb = ReplyKeyboardBuilder(
        [
            [KeyboardButton(text="добавить музыку")],
        ]
    )

    return reply_kb.as_markup(resize_keyboard=True)


def get_add_music_button(country=False):
    """Возвращает кнопки для add_music."""
    reply_kb = ReplyKeyboardBuilder()
    if country:
        reply_kb.row(KeyboardButton(text="Неизвестно"))
    reply_kb.row(KeyboardButton(text="Отмена"))

    return reply_kb.as_markup(resize_keyboard=True)
