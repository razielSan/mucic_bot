from copy import deepcopy
import asyncio
from dataclasses import dataclass
from typing import List

from aiogram import Router, F
from aiogram.filters.state import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message, ContentType

from extensions import bot
from keyboards.reply import get_add_music_button, get_music_menu_button
from error_handlers import cheak_data_is_number
from repository.executor import ExecutorSQLAlchemyRepository
from repository.album import AlbumSQLAlchemyRepository
from repository.song import SongSQLAlchemyRepository
from repository.genre import GengreSQLAlchemyRepository
from repository.user import UserSQLAlchemyRepository


router = Router()


class AddMusic(StatesGroup):
    executor = State()
    country = State()
    genre = State()
    album = State()
    year = State()
    quantity = State()
    counter = State()
    list_songs = State()
    songs = State()


@dataclass
class MusicSong:
    file_id: str
    list_songs: List


music = MusicSong(
    file_id="",
    list_songs=[],
)


@router.message(StateFilter(None), F.text == "добавить музыку")
async def start_add_music(message: Message, state: FSMContext):
    """Начало работы FSM AddMusic."""
    chat_id = message.chat.id
    message_id = message.message_id

    await bot.delete_message(chat_id=chat_id, message_id=message_id)

    await state.clear()
    await message.answer(
        "Введите название исполнителя",
        reply_markup=get_add_music_button(),
    )
    await state.set_state(AddMusic.executor)


@router.message(StateFilter("*"), F.text == "Отмена")
async def cancel_handler(message: Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return

    await state.clear()
    await message.answer("Действия отменены")
    await bot.send_message(
        chat_id=message.chat.id,
        text="Музыкальны архив",
        reply_markup=get_music_menu_button(),
    )


@router.message(AddMusic.executor, F.text)
async def add_executor(message: Message, state: FSMContext):
    """Реакция бота на введение пользователем исполнителя."""
    await state.update_data(executor=message.text.capitalize().strip())

    await message.answer(
        "Введите название страны исполнителя или нажмите 'Неизвестно'",
        reply_markup=get_add_music_button(country=True),
    )
    await state.set_state(AddMusic.country)


@router.message(AddMusic.country, F.text)
async def add_country(message: Message, state: FSMContext):
    """Реакция бота на введение пользователем cтраны исполнителя."""
    await state.update_data(country=message.text.capitalize().strip())

    data = await state.get_data()

    # Создаем и получаем пользователя
    telegram = message.chat.id
    user = UserSQLAlchemyRepository().get_user_by_id(telegram=telegram)
    if not user:
        UserSQLAlchemyRepository().create_user(
            telegram=telegram, name=message.from_user.first_name
        )
        user = UserSQLAlchemyRepository().get_user_by_id(telegram=telegram)
    # Проверяем есть ли такой исполнитель в базе данных
    executor = ExecutorSQLAlchemyRepository().get_executor_by_name_and_country(
        name=data["executor"],
        country=data["country"],
        user_id=user.id,
    )
    if executor:
        await state.set_state(AddMusic.genre)
        await state.update_data(genre=None)
        await message.answer("Жанры меняйте в информации о исполнителе\n\n")
        await add_genre(message=message, state=state)
    else:
        await message.answer(
            f"Введите жанры в котором играет исполнитель через пробел в формате\n\nВведите название альбома"
            f"металл панк-рок блюз\n"
            f"пост-панк",
            reply_markup=get_add_music_button(),
        )
        await state.set_state(AddMusic.genre)
        await state.update_data(genre=True)


@router.message(AddMusic.genre, F.text)
async def add_genre(message: Message, state: FSMContext):
    """Реакция бота на введение пользователем жанра."""
    data = await state.get_data()
    genre = data.get("genre")
    if not genre:
        pass
    else:
        print("FFFf")
        list_genres = message.text.split(" ")
        list_genres = {genre.lower() for genre in list_genres}
        await state.update_data(genre=list(list_genres))

    await message.answer("Введите название альбома")
    await state.set_state(AddMusic.album)


@router.message(AddMusic.album, F.text)
async def add_album(message: Message, state: FSMContext):
    """Реакция бота на введение пользователем названия альбома."""
    await state.update_data(album=message.text.capitalize().strip())

    await message.answer("Введите год выпуска альбома")
    await state.set_state(AddMusic.year)


@router.message(AddMusic.year, F.text)
async def add_year(message: Message, state: FSMContext):
    """Реакция бота на введение пользователем года выпуска альбома."""

    year, mess = cheak_data_is_number(
        data=message.text,
        year=True,
    )
    if not year:
        await message.answer(f"{mess['error']}\n\nВведите год выпуска альбома снова")
    else:
        print(type(year))
        await state.update_data(year=year)

        await message.answer(
            "Введите количество песен в альбоме.\n\n"
            f"Какое количество песен вы укажите столько и будет добавлено в альбом, независимо от того сколько вы скините их"
        )
        await state.set_state(AddMusic.quantity)


@router.message(AddMusic.quantity, F.text)
async def add_quantity(message: Message, state: FSMContext):
    """Реакция бота на введение пользователем количество песен в альбоме."""

    quantity, mess = cheak_data_is_number(data=message.text, quantity=True)
    if not quantity:
        await message.answer(
            f"{mess['error']}\n\nВведите количество песен в альбоме снова."
            f"\n\nКакое количество песен вы укажите столько и будет добавлено в альбом, независимо от того сколько вы скините их"
        )
    else:
        await state.update_data(quantity=quantity)

        await message.answer(
            "Скидывайте песни из альбома в количестве не более 50 штук"
        )
        await state.set_state(AddMusic.counter)
        await state.update_data(counter=0)
        await state.set_state(AddMusic.list_songs)
        await state.update_data(list_songs=[])
        await state.set_state(AddMusic.songs)


@router.message(AddMusic.songs)
async def add_songs(message: Message, state: FSMContext):
    """Реакция бота на скидывание пользователем музыки."""

    async def task():
        global music
        data = await state.get_data()
        list_songs = data["list_songs"]
        counter = data["counter"] + 1

        quantity = data["quantity"]
        list_songs.append([message.audio.file_id, message.audio.file_name])
        await state.set_state(AddMusic.counter)
        await state.update_data(counter=counter)
        await state.set_state(AddMusic.list_songs)
        await state.update_data(list_songs=list_songs)
        await state.set_state(AddMusic.songs)
        if counter == quantity:
            music.file_id = message.audio.file_id
            music.list_songs = list_songs
        return

    if message.content_type == ContentType.AUDIO:
        global music
        await asyncio.gather(task())
        data = await state.get_data()
        if message.audio.file_id == music.file_id:

            data = await state.get_data()
            executor = data["executor"]
            country = data["country"]
            # Создаем исполнителя
            list_genres = data["genre"]
            user = UserSQLAlchemyRepository().get_user_by_id(
                telegram=message.chat.id,
            )
            print(list_genres)
            if list_genres:
                for genre in list_genres:
                    GengreSQLAlchemyRepository().create_one_genre(title=genre)
                list_genres = GengreSQLAlchemyRepository().get_genres(
                    title_list=list_genres
                )

                ExecutorSQLAlchemyRepository().create_executor(
                    name=executor,
                    user=user,
                    list_genres=list_genres,
                    country=country,
                )

            executor = ExecutorSQLAlchemyRepository().get_executor_by_name_and_country(
                name=executor,
                user_id=user.id,
                country=country,
            )

            executor_name = executor.name
            executor_id = executor.id
            executor_country = executor.country

            # Создаем альбом
            album = AlbumSQLAlchemyRepository().create_album(
                title=data["album"],
                year=data["year"],
                executor_name=executor_name,
                executor_id=executor_id,
                executor_country=executor_country,
            )

            if album:
                # Создаем песни к альбому
                album = AlbumSQLAlchemyRepository().get_album(
                    executor_name=executor_name,
                    title=data["album"],
                    executor_id=executor_id,
                )
                songs = SongSQLAlchemyRepository().create_songs(
                    songs=music.list_songs,
                    album_id=album.id,
                    executor_name=executor_name,
                    executor_album=album.title,
                )
                if songs:
                    await state.clear()
                    await message.answer("Музыка успешно добавлена")
                    await bot.send_message(
                        text="Музыкальный архив",
                        reply_markup=get_music_menu_button(),
                        chat_id=message.chat.id,
                    )
                else:
                    AlbumSQLAlchemyRepository().delete_album(
                        title=album.title,
                        year=album.year,
                        executor_id=executor_id,
                    )
                    await state.clear()
                    await message.answer(
                        f"В одном альбоме не может быть двух песен с одинаковым названием"
                    )
                    await start_add_music(message=message, state=state)
            else:
                await message.answer(
                    "Исполнитель с такой страной и альбомом уже есть в музыкальном архиве"
                )
                await state.clear()
                await start_add_music(message=message, state=state)
        else:
            return

    else:
        await message.answer("Песни должны быть в аудио формате")
