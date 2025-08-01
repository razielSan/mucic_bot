from typing import List

from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton

from repository.executor import ExecutorSQLAlchemyRepository
from repository.album import AlbumSQLAlchemyRepository
from models import Executor, User, Song, Album


def get_albums_executors_button(
    executor: Executor,
    user: User,
    album=None,
    list_songs=None,
):
    """Возвращает инлайн-клавиатуру спиcка альбомов исполнителя или с отдельным альбомом со списком песен."""
    inline_kb = InlineKeyboardBuilder()

    collection = False
    album_collection_songs = False
    if executor.name == user.name and executor.country == user.name:
        collection = True
        album_collection_songs = True

    executors = ExecutorSQLAlchemyRepository().get_executors_is_user(
        user_id=user.id,
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
        if album_collection_songs:
            data = None

        inline_kb = InlineKeyboardBuilder()

        if data:
            inline_kb.add(
                InlineKeyboardButton(
                    text=data,
                    callback_data=f"album {album.id}_{executor.id}_-",
                )
            )
        for song in list_songs[0:30]:
            inline_kb.row(
                InlineKeyboardButton(
                    text=f"{song.order}. {song.name}",
                    callback_data=f"song {executor.id}_{album.id}_{song.order}",
                ),
            )

    else:
        # Логика для списка альбомов исполнителя
        albums = AlbumSQLAlchemyRepository().get_albums(executor_id=executor.id)
        for album in albums:
            inline_kb.row(
                InlineKeyboardButton(
                    text=f"🤘 {album.title}     ({album.year}) 🤘",
                    callback_data=f"album {album.id}_{executor.id}_+",
                )
            )

    if not collection:
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


def get_search_inline_button():
    """Возвращает инлайн-клавиатуру с кнопками поиска."""
    inline_kb = InlineKeyboardBuilder()
    inline_kb.row(
        InlineKeyboardButton(
            text="🔎 По Имени 🔍",
            callback_data="search_name",
        )
    )
    inline_kb.row(
        InlineKeyboardButton(
            text="🔎 По Стране 🔍",
            callback_data="search_country",
        )
    )
    inline_kb.row(
        InlineKeyboardButton(
            text="🔎 По Жанру 🔍",
            callback_data="search_genre",
        )
    )
    inline_kb.row(
        InlineKeyboardButton(
            text="🔎 Вывод Всех Исполнителей 🔍",
            callback_data="search_all",
        )
    )
    return inline_kb.as_markup(resize_keyboard=True)


def get_button_is_search_executor(
    executors_list: List[Executor],
):
    """Возвращает кнопки со списком исполнителей."""
    inline_kb = InlineKeyboardBuilder()
    for executor in executors_list:
        inline_kb.row(
            InlineKeyboardButton(
                text=f"{executor.name} ({executor.country})",
                callback_data=f"input {executor.id}",
            )
        )
    return inline_kb.as_markup(resize_keyboard=True)


def get_button_is_collection_song(
    songs_list: List[Song],
    executor: Executor,
    album: Album,
    order=0,
    back=None,
    forward=None,
):
    """Возвращает кнопки со списком песен из сборника песен."""
    inline_kb = InlineKeyboardBuilder()

    if order == 0:
        for song in songs_list[:30]:
            inline_kb.row(
                InlineKeyboardButton(
                    text=f"{song.order}.{song.name}",
                    callback_data=f"song {executor.id}_{song.album_id}_{song.order}",
                )
            )
    else:
        if forward:
            next_order = order + 30
        elif back:
            next_order = order - 30
            order = order - 60
            print(order, "back")
        print(order, "true")
        for song in songs_list[order : order + 30]:
            inline_kb.row(
                InlineKeyboardButton(
                    text=f"{song.order}.{song.name}",
                    callback_data=f"song {executor.id}_{song.album_id}_{song.order}",
                )
            )

    inline_kb.row(
        InlineKeyboardButton(
            text=f"🎸 Добавить Песни 🎸",
            callback_data=f"add_songs {executor.id}_{album.id}",
        )
    )

    if songs_list:
        inline_kb.row(
            InlineKeyboardButton(
                text=f"😢 Удалить Песни 😢",
                callback_data=f"delete_songs {executor.id}_{album.id}",
            )
        )

        if order == 0 and len(songs_list) > 30:
            inline_kb.row(
                InlineKeyboardButton(
                    text=f"Вперед 👉",
                    callback_data=f"forward_songs {executor.id}_{album.id}_30",
                )
            )
        else:
            if forward:
                data = len(songs_list) - next_order
                print(data)
                if data < 0:
                    inline_kb.row(
                        InlineKeyboardButton(
                            text=f"👈 Назад",
                            callback_data=f"back_songs {executor.id}_{album.id}_{next_order}",
                        )
                    )
                else:
                    inline_kb.row(
                        InlineKeyboardButton(
                            text=f"👈 Назад",
                            callback_data=f"back_songs {executor.id}_{album.id}_{next_order}",
                        )
                    )
                    inline_kb.add(
                        InlineKeyboardButton(
                            text=f"Вперед 👉",
                            callback_data=f"forward_songs {executor.id}_{album.id}_{next_order}",
                        )
                    )
            if back:
                print(next_order, order)
                if next_order == 0:
                    inline_kb.add(
                        InlineKeyboardButton(
                            text=f"Вперед 👉",
                            callback_data=f"forward_songs {executor.id}_{album.id}_{next_order}",
                        )
                    )
                else:
                    inline_kb.row(
                        InlineKeyboardButton(
                            text=f"👈 Назад",
                            callback_data=f"back_songs {executor.id}_{album.id}_{next_order}",
                        )
                    )
                    inline_kb.add(
                        InlineKeyboardButton(
                            text=f"Вперед 👉",
                            callback_data=f"forward_songs {executor.id}_{album.id}_{next_order}",
                        )
                    )

    return inline_kb.as_markup(resize_keyboard=True)
