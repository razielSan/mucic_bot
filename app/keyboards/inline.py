from typing import List

from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton

from repository.executor import ExecutorSQLAlchemyRepository
from models import Executor, Album


def get_albums_executors_button(
    executor: Executor,
    user_id: int,
    album=None,
    list_songs=None,
):
    """Возвращает инлайн-клавиатуру спиcка альбомов исполнителя или с отдельным альбомом со списком песен."""
    inline_kb = InlineKeyboardBuilder()

    executors = ExecutorSQLAlchemyRepository().get_executors_is_user(
        user_id=user_id,
    )
    len_executors = len(executors)
    order = 0
    for index, ex in enumerate(executors, start=1):
        if ex.name == executor.name and ex.country == executor.country:
            order = index

    delete_album = False
    if album:
        # Логика для отдельного альбома со списком песен
        delete_album = True
        left_split = "*" * 20
        right_split = "*" * 20
        data = f"{left_split}{album.title} ({album.year}){right_split}\n"

        inline_kb = InlineKeyboardBuilder()
        inline_kb.add(
            InlineKeyboardButton(
                text=data,
                callback_data=f"album {album.id}_{executor.id}_-",
            )
        )
        for song in list_songs:
            inline_kb.row(
                InlineKeyboardButton(
                    text=f"{song.order}. {song.name}",
                    callback_data=f"song {executor.id}_{album.id}_{song.order}",
                ),
            )

    else:
        print("*" * 10)
        # Логика для списка альбомов исполнителя
        for album in executor.albums:
            inline_kb.row(
                InlineKeyboardButton(
                    text=f"🤘 {album.title}     ({album.year}) 🤘",
                    callback_data=f"album {album.id}_{executor.id}_+",
                )
            )

    inline_kb.row(
        InlineKeyboardButton(
            text="🎵 Изменить Жанр Исполнителя 🎵",
            callback_data=f"update_genre {executor.id}",
        )
    )
    inline_kb.row(
        InlineKeyboardButton(
            text="🎵 Изменить Имя Исполнителя 🎵",
            callback_data=f"сhange_name {executor.id}",
        )
    )
    inline_kb.row(
        InlineKeyboardButton(
            text="🎵 Изменить Страну Исполнителя 🎵",
            callback_data=f"change_country {executor.id}",
        )
    )
    inline_kb.row(
        InlineKeyboardButton(
            text="🎸 Добавить Альбом 🎸", callback_data=f"add_album {executor.id}"
        )
    )

    inline_kb.row(
        InlineKeyboardButton(
            text="😢 Удалить Исполнителя 😢",
            callback_data=f"delete_executor {executor.id}",
        )
    )
    if delete_album:
        inline_kb.row(
            InlineKeyboardButton(
                text="😢 Удалить Aльбом 😢",
                callback_data=f"delete_album {executor.id}_{album.id}",
            )
        )        

    # Логика для подключения кнопок forward и back
    if len_executors == 1:
        pass
    elif order == 1:
        inline_kb.row(
            InlineKeyboardButton(
                text="Вперед 👉",
                callback_data=f"forward {executor.id}",
            )
        )
    elif order == len_executors:
        inline_kb.row(
            InlineKeyboardButton(text="👈 Назад", callback_data=f"back {executor.id}")
        )
    else:
        inline_kb.row(
            InlineKeyboardButton(text="👈 Назад", callback_data=f"back {executor.id}")
        )
        inline_kb.add(
            InlineKeyboardButton(
                text="Вперед 👉",
                callback_data=f"forward {executor.id}",
            )
        )

    return inline_kb.as_markup(resize_keyboard=True)
