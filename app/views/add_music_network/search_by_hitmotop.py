import os
from pathlib import Path

from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

from keyboards.reply import (
    get_add_music_button,
    get_button_for_add_music_network,
    get_music_menu_button,
)
from functions import (
    get_found_list_artists_for_hitmotop,
    get_data_names_and_title_aritists,
    download_music_to_the_path,
)
from config import settings
from extensions import bot
from error_handlers import chek_data_is_interval
from repository.user import UserSQLAlchemyRepository
from repository.album import AlbumSQLAlchemyRepository
from repository.executor import ExecutorSQLAlchemyRepository
from repository.song import SongSQLAlchemyRepository
from repository.genre import GengreSQLAlchemyRepository

router = Router(name=__name__)


class SearchHitmotop(StatesGroup):
    name = State()
    list_artists = State()
    order = State()


@router.message(F.text == "💻 Искать на сайте hitmotop 💻")
async def search_hitmotop(message: Message, state: FSMContext):
    """Работа с FSM SearchHitmotop.Просит у пользователя ввести даныые для поиска песни."""
    await message.answer(
        "Введите имя исполнителя, название песни или имя исполнителя"
        "и название песни для поиска.Песня будет добавлена в сборник песен",
        reply_markup=get_add_music_button(),
    )
    await state.set_state(SearchHitmotop.name)


@router.message(SearchHitmotop.name, F.text == "Отмена")
@router.message(SearchHitmotop.order, F.text == "Отмена")
async def cancel_search_hitmotop(message: Message, state: FSMContext):
    """Работа с FSM SearchHitmotop.Отменяет все действия."""
    current_state = await state.get_state()
    if current_state is None:
        return

    await state.clear()
    await message.answer("Поиск песен с сайта ru.hitmotop.com отменен")
    await bot.send_message(
        chat_id=message.chat.id,
        text="Музыкальный архив",
        reply_markup=get_music_menu_button(),
    )


@router.message(SearchHitmotop.name, F.text)
async def search_executor_hitmotop(message: Message, state: FSMContext):
    """Работа с FSM SearchHitmotop.Добавляет имя исполнителя, список песен в FSM.
    Просит у пользователя ввести номер песня для добавляния в сборник песен.
    """

    list_artists = get_found_list_artists_for_hitmotop(
        url=settings.HITMOTOP_SEARCH_URL,
        name=message.text,
        count=settings.COUNT_HITMOTOP,
    )
    data = get_data_names_and_title_aritists(list_artists=list_artists)

    await message.answer(text=data)
    await bot.send_message(
        chat_id=message.chat.id,
        text="Напишите номер песни которую хотите добавть в сборник песен",
    )
    await state.update_data(name=message.text)
    await state.set_state(SearchHitmotop.list_artists)
    await state.update_data(list_artists=list_artists)
    await state.set_state(SearchHitmotop.order)


@router.message(SearchHitmotop.order, F.text)
async def search_order_hitmotop(message: Message, state: FSMContext):
    """Работа с FSM SearchHitmotop.Добавляет песню в сборник песен и
    скачивает ее в media/hitmotop/<имя пользователя/.
    """
    data = await state.get_data()

    order, mess = chek_data_is_interval(
        data=message.text,
        interval=[1, len(data["list_artists"])],
    )
    if not order:
        await message.answer(
            text=f"{mess['err']}\n\nНапишите снова номер песни которую хотите добавить в сборник песен"
        )
    else:
        artist = data["list_artists"][order - 1]
        name = artist[0]
        title = artist[1]
        url = artist[2]
        dir_path = Path(__file__).parent.parent.parent
        filename = f"{name} - {title}.mp3"

        # Проверяет сущесвутует ли папка для загрузки песен у пользователя и если нет создает ее
        user = UserSQLAlchemyRepository().get_user_by_telegram(
            telegram=message.chat.id,
        )
        user_path = os.path.join(dir_path, settings.HITMOTOP_PATH, f"{user.name}")

        if not os.path.exists(user_path):
            os.mkdir(user_path)

        # Проверяет есть ли такая песня в пути
        path = os.path.join(user_path, f"{filename}")
        if os.path.exists(path):
            print("ok")
            await state.clear()
            await message.answer("Такая песня уже есть в сборнике песен")
            await search_hitmotop(
                message=message,
                state=state,
            )
        else:
            download_music_to_the_path(url=url, path=path)

            executor = ExecutorSQLAlchemyRepository().get_executor_by_name_and_country(
                name=user.name,
                country=user.name,
                user_id=user.id,
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
                title=settings.AlBUM_TITLE_COLLECTION,
                executor_id=executor.id,
            )

            # Логика для создания сборника если не создан
            if not album:
                AlbumSQLAlchemyRepository().create_album(
                    title=settings.AlBUM_TITLE_COLLECTION,
                    year=-1,
                    executor_country=executor.country,
                    executor_id=executor.id,
                    executor_name=executor.name,
                )
                album = AlbumSQLAlchemyRepository().get_album(
                    executor_id=executor.id,
                    title=settings.AlBUM_TITLE_COLLECTION,
                    executor_name=executor.name,
                )

            # Проверяет есть ли песня с таким именем в базые данных
            song = SongSQLAlchemyRepository().get_song(name=filename)
            if song:
                await state.clear()
                await message.answer("Такая песня уже есть в сборнике песен")
                await search_hitmotop(
                    message=message,
                    state=state,
                )
            else:
                song = SongSQLAlchemyRepository().get_songs(
                    album_id=album.id,
                )
                order = song[-1].order if song else 0
                SongSQLAlchemyRepository().create_songs(
                    songs=[[path, filename]],
                    album_id=album.id,
                    executor_name=executor.name,
                    order=order + 1,
                    executor_album=album.title,
                )

                await state.clear()
                await message.answer(
                    f"Песня {filename} успешно добавлена в сборник песен"
                )
                await bot.send_message(
                    chat_id=message.chat.id,
                    text="Меню поиска",
                    reply_markup=get_button_for_add_music_network(),
                )
