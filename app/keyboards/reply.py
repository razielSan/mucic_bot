from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram.types.keyboard_button import KeyboardButton


def get_music_menu_button():
    """Возвращает кнопки главного меню бота."""
    reply_kb = ReplyKeyboardBuilder(
        [
            [
                KeyboardButton(
                    text="Добавить музыку (самостоятельно)"
                ),
                KeyboardButton(text="Добавить музыку (искать в сети)"),
            ],
            [
                KeyboardButton(text="Добавить музыку в сборник песен"),
                KeyboardButton(text="Сборник песен"),
            ],
            [
                KeyboardButton(text="Cписок исполнителей"),
            ],
            [
                KeyboardButton(text="Поиск"),
            ],
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
