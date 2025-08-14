from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram.types.keyboard_button import KeyboardButton

from config import settings


def get_music_menu_button():
    """Возвращает кнопки главного меню бота."""
    reply_kb = ReplyKeyboardBuilder(
        [
            [
                KeyboardButton(text="🎼 Музыкальный архив 🎼"),
            ],
            [
                KeyboardButton(text=f"🎶 {settings.AlBUM_TITLE_COLLECTION} 🎶"),
            ],
            [
                KeyboardButton(text="💾 Добавить музыку (самостоятельно) 💾"),
                KeyboardButton(text="💾 Искать музыку в интернете 💾"),
            ],
            [
                KeyboardButton(text="💾 Добавить музыку в сборник песен 💾"),
            ],
            [
                KeyboardButton(text="🎸 Список исполнителей 🎸"),
            ],
            [
                KeyboardButton(text="🔎 Поиск 🔍"),
            ],
        ]
    )

    return reply_kb.as_markup(resize_keyboard=True)


def get_button_for_add_music_network():
    """Возвращает кнопки для поиска по сети."""
    reply_kb = ReplyKeyboardBuilder(
        [
            [
                KeyboardButton(text="💻 Список исполнителей музыкального хранилища 💻"),
            ],
            [
                KeyboardButton(text="💻 Искать в музыкальном хранилище 💻"),
            ],
            [
                KeyboardButton(text="💻 Искать на сайте hitmotop 💻"),
            ],
        ]
    )

    return reply_kb.as_markup(resize_keyboard=True)


def get_add_music_button(country=False, all_song=False):
    """Возвращает кнопки для add_music."""
    reply_kb = ReplyKeyboardBuilder()
    if country:
        reply_kb.row(KeyboardButton(text="Неизвестно"))
    if all_song:
        reply_kb.row(KeyboardButton(text="Все"))
    reply_kb.row(KeyboardButton(text="Отмена"))

    return reply_kb.as_markup(resize_keyboard=True)


def get_update_genre_executors_button():
    """Возвращает кнопки для изменения жанры исполнителя музыки."""
    reply_kb = ReplyKeyboardBuilder()
    reply_kb.row(KeyboardButton(text="<Отмена>"))

    return reply_kb.as_markup(resize_keyboard=True)


def get_delete_executor_and_album_button():
    """Возвращает кнопки для удаления исполнителя музыки."""
    reply_kb = ReplyKeyboardBuilder()
    reply_kb.row(KeyboardButton(text="Я передумал"))

    return reply_kb.as_markup(resize_keyboard=True)


def get_update_executorname_and_country_button():
    """Возвращает кнопки изменения имени пользователя или страны."""
    reply_kb = ReplyKeyboardBuilder()
    reply_kb.row(KeyboardButton(text="Отмена"))

    return reply_kb.as_markup(resize_keyboard=True)


def get_search_reply_button():
    """Возвращает кнопки для поиска."""
    reply_kb = ReplyKeyboardBuilder()
    reply_kb.row(KeyboardButton(text="Отмена"))

    return reply_kb.as_markup(resize_keyboard=True)


def get_buttons_is_add_music_newtork(
    all_album=False,
    forward=False,
):
    """Возвращает кнопки для выбора всех альбомов и отмены поиска."""
    reply_kb = ReplyKeyboardBuilder()
    if all_album:
        reply_kb.row(KeyboardButton(text="Все"))
    if forward:
        reply_kb.row(KeyboardButton(text="Дальше"))
    reply_kb.row(KeyboardButton(text="Отмена"))
    return reply_kb.as_markup(resize_keyboard=True)


def get_menu_admin():
    """Возвращает кнопки меню для администратора."""
    reply_kb = ReplyKeyboardBuilder()
    reply_kb.row(
        KeyboardButton(text="Обновить список исполнителей для музыкального хранилища")
    )

    return reply_kb.as_markup(resize_keyboard=True)
