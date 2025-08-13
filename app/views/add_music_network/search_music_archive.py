import os

from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

from config import settings
from extensions import bot
from functions import get_list_albums_executors
from keyboards.reply import get_buttons_is_add_music_newtork, get_music_menu_button
from repository.executor import ExecutorSQLAlchemyRepository
from repository.user import UserSQLAlchemyRepository
from repository.genre import GengreSQLAlchemyRepository
from repository.album import AlbumSQLAlchemyRepository
from repository.song import SongSQLAlchemyRepository
from error_handlers import cheak_data_is_number


router = Router(name=__name__)


class AddMusicNetwork(StatesGroup):
    """Класс для добавления музыки по сети."""

    executor = State()
    temp = State()  # данные нужные для того чтобы пропустить ввод имени исполнителя
    country_update = (
        State()
    )  # данные нужные для сохранения страны исполнителя если альбомы уже
    # есть в музыкальном архиве
    country = State()
    genre = State()
    list_albums = State()
    full_path = State()


@router.message(F.text == "💻 Искать в музыкальном хранилище 💻")
async def add_music_newtork(message: Message, state: FSMContext):
    """FSM AddMusicNetwork. Просить у пользователя ввести имя исполнителя."""

    await state.clear()
    await message.answer(
        "Введите имя исполнителя", reply_markup=get_buttons_is_add_music_newtork()
    )

    await state.set_state(AddMusicNetwork.executor)


@router.message(AddMusicNetwork.full_path, F.text == "Отмена")
@router.message(AddMusicNetwork.executor, F.text == "Отмена")
@router.message(AddMusicNetwork.temp, F.text == "Отмена")
@router.message(AddMusicNetwork.country, F.text == "Отмена")
async def cancel_executor_network(message: Message, state: FSMContext):
    """FSM AddMusicNetwork. Отменяет все дейстия."""
    current_state = await state.get_state()

    if current_state is None:
        return

    await state.clear()
    await message.answer(text="Скачивание из музыкального архива отменено")
    await bot.send_message(
        text="Музыкальный архим",
        chat_id=message.chat.id,
        reply_markup=get_music_menu_button(),
    )


@router.message(AddMusicNetwork.executor, F.text)
async def add_executor_network(message: Message, state: FSMContext):
    """FSM AddMusicNetwork. Просит у пользователя ввести имя исполнителя."""
    executor = message.text

    # Проходимся по каталогу с музыкой и ищем совпадение исполнителя
    path = ""
    for dirpath, dirname, filename in os.walk(top=f"{settings.MUSIC_PATH}"):

        data = dirpath.split("\\")
        data = data[-1]
        if executor.lower() == data.split("(")[0].strip().lower():
            path = dirpath
            break
    if path:
        # Проходися по исполнителю и добываем имя исполнителя, страну, список альбомов и путь до альбомов
        index = 0
        list_albums = []
        executor = ""
        full_path = ""
        for dirpath, dirname, filename in os.walk(top=f"{path}"):
            if index == 0:
                index += 1
                executor = dirpath.split("\\")[-1]
                full_path = dirpath
                list_albums = dirname
            index += 1
        executor, country = executor.split("(")
        executor = executor.strip()
        country = country.strip(")")

        await state.update_data(executor=executor)
        await state.set_state(AddMusicNetwork.country)
        await state.update_data(country=country)
        await state.set_state(AddMusicNetwork.list_albums)
        await state.update_data(list_albums=list_albums)
        await state.set_state(AddMusicNetwork.genre)
        await state.update_data(genre=full_path.split("\\")[-2].lower())
        await state.set_state(AddMusicNetwork.full_path)
        await state.update_data(full_path=full_path)

        data = await state.get_data()

        await message.answer(f"Найденный исполнитель\n\n{executor} ({country})")
        await bot.send_message(
            chat_id=message.chat.id,
            text="Введите имя исполнителя"
            " точно такое же как написано в музыкальном хранилище или нажмите 'Дальше'",
            reply_markup=get_buttons_is_add_music_newtork(forward=True),
        )
        await state.set_state(AddMusicNetwork.temp)

    else:
        await message.answer("Указанный исполнитель не найден")


@router.message(AddMusicNetwork.temp, F.text)
async def add_executor_handler(message: Message, state: FSMContext):
    """FSM AddMusicNetwork. Просит у пользователя ввести страну исполнителя."""

    if message.text != "Дальше":
        await state.set_state(AddMusicNetwork.executor)
        await state.update_data(executor=message.text)

    await message.answer(
        text="Введите страну исполнителя"
        " точно такую же как написано в музыкальном хранилище или нажмите 'Дальше'",
    )
    await state.set_state(AddMusicNetwork.country)


@router.message(AddMusicNetwork.country, F.text)
async def add_country_handler(message: Message, state: FSMContext):
    """FSM AddMusicNetwork. Просит у пользователя ввести номер альбома исполнителя."""

    data = await state.get_data()
    if data.get("country_update"):
        await state.update_data(country=data["country_update"])
    elif message.text != "Дальше":
        await state.update_data(country=message.text)

    data = await state.get_data()

    albums = get_list_albums_executors(list_albums=data["list_albums"])

    await bot.send_message(
        chat_id=message.chat.id, text=f"Найденные альбомы\n\n{albums}"
    )
    await bot.send_message(
        chat_id=message.chat.id,
        text="Введите номера альбомов "
        "которые хотите в формате\n\n0.1.4\n\n"
        "Нажмите 'Все' чтобы скачать все альбомы",
        reply_markup=get_buttons_is_add_music_newtork(all_album=True),
    )
    await state.set_state(AddMusicNetwork.full_path)


@router.message(AddMusicNetwork.full_path, F.text)
async def add_full_path(message: Message, state: FSMContext):

    data = await state.get_data()
    full_path = data["full_path"]
    list_albums = data["list_albums"]
    executor = data["executor"]
    country = data["country"]
    genre = data["genre"]

    if message.text == "Все":
        list_number = [number for number in range(1, len(list_albums) + 1)]
    else:
        list_number = message.text.split(".")
        for number in list_number:
            result, mess = cheak_data_is_number(number)
            if isinstance(result, int):
                if result > len(list_albums):
                    await message.answer(
                        text="Введеного вами номера альбома нету в списке альбомов\n\n"
                        "Введите номера альбомов "
                        "которые хотите скачать через пробел в формате\n\n0.1.4\n\n"
                        "Нажмите 'Все' чтобы скачать все альбомы",
                    )
                    return
            elif not result:
                await message.answer(
                    text="Введеные данные должны не равнятся нулю,быть целыми, положительными числами\n\n"
                    "Введите номера альбомов "
                    "которые хотите скачать через пробел в формате\n\n0.1.4\n\n"
                    "Нажмите 'Все' чтобы скачать все альбомы",
                )
                return

    # Достаем лист с песнями
    list_songs = []
    for album in list_albums:
        path = "\\".join([full_path, album])
        for dirpath, dirname, filename in os.walk(top=path):
            list_songs.append([dirpath, filename])

    user = UserSQLAlchemyRepository().get_user_by_telegram(
        telegram=message.chat.id,
    )

    if not user:
        UserSQLAlchemyRepository().create_user(telegram=message.chat.id, name=message.from_user.first_name)
        user = UserSQLAlchemyRepository().get_user_by_telegram(telegram=message.chat.id)

    search_executor = ExecutorSQLAlchemyRepository().get_executor_by_name_and_country(
        user_id=user.id,
        name=executor,
        country=country,
    )

    # Создает исполнителя с жанром если нет такого
    if not search_executor:
        list_genres = GengreSQLAlchemyRepository().get_genres(title_list=[genre])
        if not list_genres:
            GengreSQLAlchemyRepository().create_one_genre(title=genre)
        list_genres = GengreSQLAlchemyRepository().get_genres(title_list=[genre])
        ExecutorSQLAlchemyRepository().create_executor(
            name=executor,
            user=user,
            list_genres=list_genres,
            country=country,
        )

    list_number = [int(number) for number in list_number]
    executor = ExecutorSQLAlchemyRepository().get_executor_by_name_and_country(
        user_id=user.id,
        name=executor,
        country=country,
    )

    order = 0  #
    list_order = []

    # Проходимся по листу с песнями
    for dirpath, filename in list_songs:
        order += 1
        if order in list_number:
            data = dirpath.split("\\")[-1]
            executor_data = data.split(')')
            album_year = executor_data[0].strip("( ")
            album_title = "".join(executor_data[1:]).strip(" -")
            songs_list = []
            songs_jpg = []

            # Добавляем в массивы данные содержащие .mp3 и .jpg а также путь до песни
            for name in filename:
                data = name.split(".")[-1].lower()
                if data in settings.MUSIC_FORMAT_LIST:
                    song_path = "\\".join([dirpath, name])
                    songs_list.append([song_path, name])
                elif data in settings.IMG_FORMAT_LIST:
                    img = "\\".join([dirpath, name])
                    songs_jpg.append(img)

            img = "Здесь скоро появится изображение"
            if songs_jpg:
                img = songs_jpg[0]
            
            album_create = AlbumSQLAlchemyRepository().create_album(
                title=album_title,
                year=int(album_year),
                executor_country=executor.country,
                executor_name=executor.name,
                executor_id=executor.id,
                img=img,
            )

            if album_create:
                album = AlbumSQLAlchemyRepository().get_album(
                    executor_name=executor.name,
                    title=album_title,
                    executor_id=executor.id,
                )
                songs = SongSQLAlchemyRepository().create_songs(
                    songs=songs_list,
                    album_id=album.id,
                    executor_album=album.title,
                    executor_name=executor.name,
                )
                if songs:
                    list_order.append(str(order))

    if list_order:
        data = ", ".join(list_order)
        await message.answer(
            f"{executor.name} с номерами альбомов {data} был добавлен в музыкальный архив"
        )
        await bot.send_message(
            chat_id=message.chat.id,
            text="Музыкальный архив",
            reply_markup=get_music_menu_button(),
        )
        await state.clear()
    else:
        await state.set_state(AddMusicNetwork.country_update)
        await state.update_data(country_update=country)
        await state.set_state(AddMusicNetwork.country)
        await message.answer("Указанные альбомы есть в музыкальном архиве")
        await add_country_handler(message=message, state=state)
