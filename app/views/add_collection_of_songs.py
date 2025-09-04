import asyncio
from dataclasses import dataclass
from typing import List

from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message, ContentType
from aiogram.filters import StateFilter

from extensions import bot
from keyboards.reply import get_add_music_button, get_music_menu_button
from error_handlers import cheak_data_is_number
from repository.executor import ExecutorSQLAlchemyRepository
from repository.album import AlbumSQLAlchemyRepository
from repository.song import SongSQLAlchemyRepository
from repository.genre import GengreSQLAlchemyRepository
from repository.user import UserSQLAlchemyRepository
from config import settings


router = Router(name=__name__)


class AddCollectionSong(StatesGroup):
    """FSM для добавления песен в сборник"""

    counter = State()
    list_songs = State()
    title = State()
    year = State()
    quantity = State()
    song = State()


@dataclass
class MusicSong:
    """Класс для хранения file_id песни и списка песен альбома исполнителя."""

    file_id: str
    list_songs: List


music = MusicSong(
    file_id="",
    list_songs=[],
)


@router.message(StateFilter(None), F.text == "💾 Добавить музыку в сборник песен 💾")
async def start_add_collection_song(message: Message, state: FSMContext):
    """FSM AddCollectionSong.Просит у пользователя ввести количество песен которые он хочет скинуть."""

    await state.clear()

    await message.answer(
        "Введите количество песен которые хотите скинуть.Количество песен должно быть не более 30 штук",
        reply_markup=get_add_music_button(),
    )
    await state.set_state(AddCollectionSong.counter)
    await state.update_data(counter=0)
    await state.set_state(AddCollectionSong.list_songs)
    await state.update_data(list_songs=[])
    await state.set_state(AddCollectionSong.title)
    await state.update_data(title=settings.AlBUM_TITLE_COLLECTION)
    await state.set_state(AddCollectionSong.year)
    await state.update_data(year=-1)
    await state.set_state(AddCollectionSong.quantity)


@router.message(AddCollectionSong.song, F.text == "Отмена")
@router.message(AddCollectionSong.quantity, F.text == "Отмена")
async def cancel_add_collection_song(message: Message, state: FSMContext):
    """Отменяет добавление песен в сборник."""
    current_state = await state.get_state()
    if current_state is None:
        return

    await state.clear()
    await message.answer("Добавление песен в сборник отменено")
    await bot.send_message(
        chat_id=message.chat.id,
        text="Музыкальный архив",
        reply_markup=get_music_menu_button(),
    )


@router.message(AddCollectionSong.quantity, F.text)
async def add_collection_quantity(message: Message, state: FSMContext):
    """FSM AddCollectionSong.Просит у пользователя скинуть песни для добавления в сборник песен."""
    quantity, mess = cheak_data_is_number(data=message.text, quantity=30)
    if not quantity:
        await message.answer(
            f"{mess['error']}\n\nВведите снова количество"
            "песен которые хотите скинуть.Количество песен должно быть не более 30 штук"
        )
    else:
        await message.answer(
            "Скидывайте песни которые хотите добавить в сборник не более 30 штук"
        )
        await state.set_state(AddCollectionSong.quantity)
        await state.update_data(quantity=quantity)
        await state.set_state(AddCollectionSong.song)


@router.message(AddCollectionSong.song)
async def finish_add_collection_song(message: Message, state: FSMContext):
    """FSM AddCollectionSong.Добавляет песни в сборник."""

    async def task():
        """Задача для проверки указанного количества песен с количеством скинутых песен."""
        global music
        try:
            data = await state.get_data()
            counter = data["counter"] + 1
            list_songs = data["list_songs"]
            quantity = data["quantity"]
            list_songs.append([message.audio.file_id, message.audio.file_name])

            await state.set_state(AddCollectionSong.counter)
            await state.update_data(counter=counter)
            await state.set_state(AddCollectionSong.list_songs)
            await state.update_data(list_songs=list_songs)
            await state.set_state(AddCollectionSong.song)

            if counter == quantity:
                music.list_songs = list_songs
                music.file_id = message.audio.file_id
            return
        except Exception as err:
            print(err)
            return

    if message.content_type == ContentType.AUDIO:
        global music

        await asyncio.gather(task())
        data = await state.get_data()
        if data.get("counter", 0) > 30:
            await state.clear()
            await message.answer("Количество песен не должно превышать 30")
            await start_add_collection_song(message=message, state=state)
            return
        if message.audio.file_id == music.file_id:
            data = await state.get_data()
            if data.get("counter") == 0:
                await state.clear()
                return
            if data.get("counter", 0) > 30:
                await state.clear()
                await message.answer("Количество песен не должно превышать 30")
                await start_add_collection_song(message=message, state=state)
                return

            user = UserSQLAlchemyRepository().get_user_by_telegram(
                telegram=message.chat.id,
            )

            if not user:
                UserSQLAlchemyRepository().create_user(
                    telegram=message.chat.id,
                    name=message.from_user.first_name,
                )
                user = UserSQLAlchemyRepository().get_user_by_telegram(
                    telegram=message.chat.id
                )

            executor = ExecutorSQLAlchemyRepository().get_executor_by_name_and_country(
                name=user.name, country=user.name, user_id=user.id
            )
            # Логика для создания исполнителя если не создан
            if not executor:
                genre = GengreSQLAlchemyRepository().get_genres(
                    title_list=["сборник"],
                )
                if not genre:
                    GengreSQLAlchemyRepository().create_one_genre(title="сборник")
                    genre = GengreSQLAlchemyRepository().get_genres(
                        title_list=["сборник"],
                    )

                ExecutorSQLAlchemyRepository().create_executor(
                    name=user.name,
                    user=user,
                    list_genres=genre,
                    country=user.name,
                )

                executor = (
                    ExecutorSQLAlchemyRepository().get_executor_by_name_and_country(
                        name=user.name, country=user.name, user_id=user.id
                    )
                )

            album = AlbumSQLAlchemyRepository().get_album(
                executor_name=executor.name,
                title=data["title"],
                executor_id=executor.id,
            )
            # Логика для создания сборника если не создан
            if not album:
                AlbumSQLAlchemyRepository().create_album(
                    title=data["title"],
                    year=data["year"],
                    executor_country=executor.country,
                    executor_id=executor.id,
                    executor_name=executor.name,
                )
                album = AlbumSQLAlchemyRepository().get_album(
                    executor_id=executor.id,
                    title=data["title"],
                    executor_name=executor.name,
                )

            songs = SongSQLAlchemyRepository().get_songs(album_id=album.id)

            # Логика для добавление песен в альбом
            list_songs = data["list_songs"]
            order = 1
            if songs:
                order = songs[-1].order + 1
            result = SongSQLAlchemyRepository().create_songs(
                songs=list_songs,
                album_id=album.id,
                executor_name=executor.name,
                executor_album=album.title,
                order=order,
            )
            if result:
                await state.clear()
                await message.answer("Песни успешно добавлены в сборник")
                await bot.send_message(
                    chat_id=message.chat.id,
                    text="Музыкальный архив",
                    reply_markup=get_music_menu_button(),
                )
            else:
                await state.clear()
                await message.answer("Песни с таким именем уже есть в сборнике")
                await start_add_collection_song(message=message, state=state)

    else:
        await message.answer(
            "Скидываемые песни должные быть в аудио формате\n\n"
            "Скидывайте снова песни которые хотите добавить в сборник не более 30 штук"
        )
