from copy import deepcopy

from aiogram import Router, F
from aiogram.types import CallbackQuery, Message, ReplyKeyboardRemove
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.types.input_file import FSInputFile
from aiogram.filters import StateFilter

from repository.executor import ExecutorSQLAlchemyRepository
from repository.album import AlbumSQLAlchemyRepository
from repository.genre import GengreSQLAlchemyRepository
from repository.song import SongSQLAlchemyRepository
from repository.user import UserSQLAlchemyRepository
from repository.genreExecutor import GenreExecutorSQLAlchemyRepository
from functions import get_info_executors, get_executor_is_button
from keyboards.inline import get_albums_executors_button
from keyboards.reply import (
    get_update_genre_executors_button,
    get_delete_executor_and_album_button,
    get_update_executorname_and_country_button,
)
from extensions import bot
from views.add_music import AddMusic, add_genre
from config import settings


router = Router(name=__name__)


@router.message(StateFilter(None), F.text == "🎼 Музыкальный архив 🎼")
async def get_executors_information(message: Message):
    """Возвращает информацию о исполнителе."""

    telegram = message.chat.id

    user = UserSQLAlchemyRepository().get_user_by_telegram(telegram=telegram)
    if not user:
        UserSQLAlchemyRepository().create_user(
            telegram=telegram, name=message.from_user.first_name
        )
        user = UserSQLAlchemyRepository().get_user_by_telegram(telegram=telegram)

    executors = ExecutorSQLAlchemyRepository().get_executors_is_user(
        user_id=user.id,
    )

    if executors:
        executor = executors[0]
        data_executor = get_info_executors(
            executor=executor,
            user=user,
        )

        # Проверяет является ли альбом сборником песен
        album = None
        list_songs = None
        if executor.name == user.name and executor.country == user.name:
            album = AlbumSQLAlchemyRepository().get_album(
                executor_name=user.name,
                title=settings.AlBUM_TITLE_COLLECTION,
                executor_id=executor.id,
            )
            list_songs = SongSQLAlchemyRepository().get_songs(album_id=album.id)

        await bot.send_message(
            chat_id=message.chat.id,
            reply_markup=ReplyKeyboardRemove(),
            text="Музыкальный архив",
        )
        await message.answer(
            text=data_executor,
            reply_markup=get_albums_executors_button(
                executor=executor, user=user, album=album, list_songs=list_songs
            ),
        )
    else:
        await message.answer(
            "У вас нет добавленых исполнителей",
            reply_markup=ReplyKeyboardRemove(),
        )


@router.callback_query(F.data.startswith("forward ") | F.data.startswith("back "))
async def get_executors_information_when_you_press_the_button(call: CallbackQuery):
    """Возвращает информацию о исполнителе при нажатии кнопок назад или вперед."""
    button, executor_id = call.data.split(" ")

    forward = True if button == "forward" else False
    back = True if button == "back" else False

    user = UserSQLAlchemyRepository().get_user_by_telegram(
        telegram=call.message.chat.id,
    )

    executor = get_executor_is_button(
        executor_id=int(executor_id),
        user=user,
        forward=forward,
        back=back,
    )
    data_executor = get_info_executors(executor=executor, user=user)

    # Проверяет является ли альбом сборником песен
    album = None
    list_songs = None
    if executor.name == user.name and executor.country == user.name:
        album = AlbumSQLAlchemyRepository().get_album(
            executor_name=user.name,
            title=settings.AlBUM_TITLE_COLLECTION,
            executor_id=executor.id,
        )
        if album:
            list_songs = SongSQLAlchemyRepository().get_songs(album_id=album.id)

    await bot.edit_message_text(
        text=data_executor,
        reply_markup=get_albums_executors_button(
            executor=executor, user=user, album=album, list_songs=list_songs
        ),
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        inline_message_id=call.id,
    )


@router.callback_query(F.data.startswith("album "))
async def get_album_songs(call: CallbackQuery):
    """Возвращает список песен для альбома."""
    _, data = call.data.split(" ")

    album_id, executor_id, move = data.split("_")

    user = UserSQLAlchemyRepository().get_user_by_telegram(
        telegram=call.message.chat.id,
    )
    executor = ExecutorSQLAlchemyRepository().get_executor_by_id(
        id=int(executor_id),
        user_id=user.id,
    )

    album = AlbumSQLAlchemyRepository().get_album_is_id(
        executor_id=executor.id,
        album_id=int(album_id),
    )

    if not album:
        await bot.send_message(
            chat_id=call.message.chat.id,
            text="Альбом был удален из музыкального архива",
        )
    else:
        list_songs = SongSQLAlchemyRepository().get_songs(album_id=album.id)

        data_executor = get_info_executors(executor=executor, user=user)

        album = album if move == "+" else None
        list_songs = list_songs if move == "+" else None

        await bot.edit_message_text(
            text=data_executor,
            reply_markup=get_albums_executors_button(
                user=user,
                executor=executor,
                album=album,
                list_songs=list_songs,
            ),
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
        )


@router.callback_query(F.data.startswith("SongsAlbums "))
async def get_list_songs_album_by_forward_or_back(call: CallbackQuery):
    """Возвращает список песен из альбома при нажатии кнопок вперед или назад."""
    _, flag, executor_id, album_id, song_position = call.data.split(" ")

    user = UserSQLAlchemyRepository().get_user_by_telegram(
        telegram=call.message.chat.id,
    )

    executor = ExecutorSQLAlchemyRepository().get_executor_by_id(
        id=int(executor_id), user_id=user.id
    )

    album = AlbumSQLAlchemyRepository().get_album_is_id(
        album_id=int(album_id),
        executor_id=executor.id,
    )

    data_executor = get_info_executors(executor=executor, user=user)
    list_songs = SongSQLAlchemyRepository().get_songs(album_id=album.id)

    await bot.edit_message_text(
        text=data_executor,
        reply_markup=get_albums_executors_button(
            user=user,
            executor=executor,
            album=album,
            list_songs=list_songs,
            song_position=int(song_position),
        ),
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
    )


@router.callback_query(F.data.startswith("song "))
async def get_song_play(call: CallbackQuery):
    """Возвращает песню для воспроизведения."""
    _, data = call.data.split(" ")
    executor_id, album_id, order = data.split("_")

    user = UserSQLAlchemyRepository().get_user_by_telegram(
        telegram=call.message.chat.id,
    )
    executor = ExecutorSQLAlchemyRepository().get_executor_by_id(
        id=int(executor_id),
        user_id=user.id,
    )

    album = AlbumSQLAlchemyRepository().get_album_is_id(
        album_id=int(album_id),
        executor_id=executor.id,
    )

    if not album:
        await bot.send_message(
            chat_id=call.message.chat.id,
            text="Песня была удалена из музыкального архива",
        )
    else:
        song_data = ""
        for song in album.songs:
            if song.order == int(order):
                song_data = song

        # Проверяет является ли аудио загруженным в телеграме или загружать из сервера
        if not song_data:
            await bot.send_message(
                chat_id=call.message.chat.id,
                text="Песня была удалени из музыкального архива",
            )
        else:
            if song_data.file_id.startswith("D:\\"):
                await call.message.answer_audio(
                    audio=FSInputFile(path=song_data.file_id),
                    caption=song_data.name,
                )
            else:
                await call.message.answer_audio(
                    audio=song_data.file_id,
                    caption=song_data.name,
                )


# Логика для обновления жанра
class UpdateGenre(StatesGroup):
    """FSM для обновления жанра исполнителя музыки."""

    executor_id = State()
    genre_list = State()


@router.callback_query(F.data.startswith("update_genre "))
async def start_update_genre(call: CallbackQuery, state: FSMContext):
    """Реакция на нажатие кнопки update_genre."""
    _, executor_id = call.data.split(" ")

    await state.clear()
    await state.set_state(UpdateGenre.executor_id)
    await state.update_data(executor_id=int(executor_id))

    await call.message.answer(
        text="Введите жанры в котором играет исполнитель через пробел в формате\n\n"
        "металл панк-рок блюз",
        reply_markup=get_update_genre_executors_button(),
    )

    await state.set_state(UpdateGenre.genre_list)


@router.message(UpdateGenre.genre_list, F.text == "<Отмена>")
async def genre_cancel_handler(message: Message, state: FSMContext):
    """Отмена обновления жанра."""
    current_state = await state.get_state()
    if current_state is None:
        return

    await state.clear()
    await message.answer(
        "Обновление жанра отменено",
        reply_markup=ReplyKeyboardRemove(),
    )
    await get_executors_information(message=message)


@router.message(UpdateGenre.genre_list, F.text)
async def finish_update_genre(message: Message, state: FSMContext):
    """Реакция на введение пользователем жанра для обновления."""
    genres = set(message.text.split(" "))
    data = await state.get_data()
    user = UserSQLAlchemyRepository().get_user_by_telegram(
        telegram=message.chat.id,
    )

    genres_set = GengreSQLAlchemyRepository().get_all_genre()
    GengreSQLAlchemyRepository().get_genres(title_list=list(genres))

    genres_list_update = deepcopy(genres)

    genres.difference_update(genres_set)
    if genres:
        GengreSQLAlchemyRepository().create_many_genre(title_list=list(genres))

    genres_list_update = GengreSQLAlchemyRepository().get_genres(
        title_list=genres_list_update
    )

    GenreExecutorSQLAlchemyRepository().delete_executor_genre(
        executor_id=data["executor_id"]
    )
    for genre in genres_list_update:
        GenreExecutorSQLAlchemyRepository().executor_genre(
            executor_id=data["executor_id"], genre_id=genre.id
        )

    await state.clear()
    await message.answer(
        "Жанр успешно изменен",
        reply_markup=ReplyKeyboardRemove(),
    )
    await get_executors_information(message=message)


# Логика для удаления исполнителя
class DeleteExecutor(StatesGroup):
    """FSM для удаления исполнителя."""

    executor_id = State()


@router.callback_query(F.data.startswith("delete_executor "))
async def start_delete_executor(call: CallbackQuery, state: FSMContext):
    """Реакция на нажатие кнопки delete_executor."""
    _, executor_id = call.data.split(" ")

    await state.clear()
    await state.set_state(DeleteExecutor.executor_id)
    await state.update_data(executor_id=int(executor_id))

    await call.message.answer(
        "Вы уверены что хотите удалить исполнителя ?Наберите любой символ если хотите удалить исполнителя или нажмите 'Я передумал'",
        reply_markup=get_delete_executor_and_album_button(),
    )


@router.message(DeleteExecutor.executor_id, F.text)
async def finish_delete_executor(message: Message, state: FSMContext):
    """Реакция на введние пользователем иполнителя на удаление."""
    result = message.text
    if result == "Я передумал":
        await state.clear()
        await message.answer(
            "Удаление исполнителя отменено",
            reply_markup=ReplyKeyboardRemove(),
        )
        await get_executors_information(message=message)
    else:
        data = await state.get_data()
        user = UserSQLAlchemyRepository().get_user_by_telegram(telegram=message.chat.id)
        AlbumSQLAlchemyRepository().delete_all_albums(executor_id=data["executor_id"])
        ExecutorSQLAlchemyRepository().delete_executor_is_id(
            user_id=user.id,
            executor_id=data["executor_id"],
        )

        await state.clear()
        await message.answer(
            "Исполнитель успешно удален из музыкального архива",
            reply_markup=ReplyKeyboardRemove(),
        )
        await get_executors_information(message=message)


# Логика для добавления исполнителя
# Перебрасывает на функцию add_genre
@router.callback_query(F.data.startswith("add_album "))
async def add_album_is_executor(call: CallbackQuery, state: FSMContext):
    """Реакция на нажатие кнопки add_album."""
    _, executor_id = call.data.split(" ")
    user = UserSQLAlchemyRepository().get_user_by_telegram(
        telegram=call.message.chat.id,
    )
    executor = ExecutorSQLAlchemyRepository().get_executor_by_id(
        id=int(executor_id),
        user_id=user.id,
    )

    await state.clear()
    await state.set_state(AddMusic.executor)
    await state.update_data(executor=executor.name)
    await state.set_state(AddMusic.country)
    await state.update_data(country=executor.country)
    await state.set_state(AddMusic.genre)
    await state.update_data(genre=None)

    await add_genre(state=state, message=call.message)


# Логика для изменения имя исполнителя
class UpdateNameExecutor(StatesGroup):
    """FSM для изменения имени исполнителя."""

    executor_id = State()
    name_executor = State()


@router.callback_query(F.data.startswith("сhange_name "))
async def change_executor_name(call: CallbackQuery, state: FSMContext):
    """Реакция на кнопку change_name."""
    _, executor_id = call.data.split(" ")

    await state.clear()
    await state.set_state(UpdateNameExecutor.executor_id)
    await state.update_data(executor_id=int(executor_id))
    await state.set_state(UpdateNameExecutor.name_executor)

    await call.message.answer(
        "Введите новое имя исполнителя",
        reply_markup=get_update_executorname_and_country_button(),
    )


@router.message(UpdateNameExecutor.name_executor, F.text == "Отмена")
async def cancel_change_name_handler(message: Message, state: FSMContext):
    """Отменяет изменение имени исполнителя."""
    current_state = await state.get_state()
    if current_state is None:
        return

    await state.clear()
    await message.answer(
        "Изменение имя исполнителя отменено",
        reply_markup=ReplyKeyboardRemove(),
    )
    await get_executors_information(message=message)


@router.message(UpdateNameExecutor.name_executor, F.text)
async def name_executor(message: Message, state: FSMContext):
    """Реакция на введение пользователем нового имени исполнителя."""
    executor_name = message.text
    data = await state.get_data()

    user = UserSQLAlchemyRepository().get_user_by_telegram(
        telegram=message.chat.id,
    )
    executor = ExecutorSQLAlchemyRepository().get_executor_by_id(
        user_id=user.id,
        id=int(data["executor_id"]),
    )
    ExecutorSQLAlchemyRepository().update_name(
        execotor_name=executor_name,
        user_id=user.id,
        executor_id=executor.id,
    )
    AlbumSQLAlchemyRepository().update_executor_name_is_album(
        executor_id=executor.id, executor_name=executor_name
    )

    album_list_id = []
    for album in executor.albums:
        album_list_id.append(album.id)

    SongSQLAlchemyRepository().update_executor_name_is_song(
        list_albums_id=album_list_id,
        executor_name=executor_name,
    )

    await state.clear()
    await message.answer(
        "Имя исполнителя успешно изменено", reply_markup=ReplyKeyboardRemove()
    )
    await get_executors_information(message=message)


# Логика для изменения альбома исполнителя
class ChangeAlbumExecutor(StatesGroup):
    """FSM для изменения альбома исполнителя."""

    executor_id = State()
    album_id = State()
    title = State()


@router.callback_query(F.data.startswith("change_album "))
async def change_album_title(call: CallbackQuery, state: FSMContext):
    """Работа с FSM ChangeAlbumExecutor.Просит пользователя ввести новое имя для альбома."""
    _, executor_id, album_id = call.data.split(" ")

    await state.clear()
    await state.set_state(ChangeAlbumExecutor.executor_id)
    await state.update_data(executor_id=int(executor_id))
    await state.set_state(ChangeAlbumExecutor.album_id)
    await state.update_data(album_id=int(album_id))

    await call.message.answer(
        "Введите новое название для альбома",
        reply_markup=get_update_executorname_and_country_button(),
    )

    await state.set_state(ChangeAlbumExecutor.title)


@router.message(ChangeAlbumExecutor.title, F.text == "Отмена")
@router.message(ChangeAlbumExecutor.executor_id, F.text == "Отмена")
@router.message(ChangeAlbumExecutor.album_id, F.text == "Отмена")
async def cancel_change_album_title_handler(message: Message, state: FSMContext):
    """Работа с FSM ChangeAlbumExecutor.Отменяет изменение название албома."""
    current_state = await state.get_state()
    if current_state is None:
        return

    await state.clear()
    await message.answer(
        "Изменение Названия Альбома Отеменено",
        reply_markup=ReplyKeyboardRemove(),
    )
    await get_executors_information(message=message)


@router.message(ChangeAlbumExecutor.title, F.text)
async def finish_change_album_title(message: Message, state: FSMContext):
    """Работа с FSM ChangeAlbumExecutor.Изменяет название альбома."""
    data = await state.get_data()
    executor_id = data["executor_id"]
    album_id = data["album_id"]
    album_tilte = message.text

    AlbumSQLAlchemyRepository().update_title_is_album(
        album_id=album_id, executor_id=executor_id, title=album_tilte
    )

    SongSQLAlchemyRepository().update_executor_album_is_song(
        album_id=album_id,
        executor_album=album_tilte,
    )

    await state.clear()
    await message.answer(
        "Название альбома успешно изменено", reply_markup=ReplyKeyboardRemove()
    )
    await get_executors_information(message=message)


# Логика для изменения страны исполнителя
class UpdateCountryExecutor(StatesGroup):
    """FSM для изменения страны исполнителя."""

    executor_id = State()
    country_executor = State()


@router.callback_query(F.data.startswith("change_country "))
async def change_executor_country(call: CallbackQuery, state: FSMContext):
    """Реакция на кнопку change_country."""
    _, executor_id = call.data.split(" ")

    await state.clear()
    await state.set_state(UpdateCountryExecutor.executor_id)
    await state.update_data(executor_id=int(executor_id))
    await state.set_state(UpdateCountryExecutor.country_executor)

    await call.message.answer(
        "Введите новое название страны для исполнителя.",
        reply_markup=get_update_executorname_and_country_button(),
    )


@router.message(UpdateCountryExecutor.country_executor, F.text == "Отмена")
async def cancel_change_country_handler(message: Message, state: FSMContext):
    """Отмена изменения страны исполнителя."""
    current_state = await state.get_state()
    if current_state is None:
        return

    await state.clear()
    await message.answer(
        "Изменение страны исполнителя отменено",
        reply_markup=ReplyKeyboardRemove(),
    )
    await get_executors_information(message=message)


@router.message(UpdateCountryExecutor.country_executor, F.text)
async def country_executorr(message: Message, state: FSMContext):
    """Реакция на введение пользователем нового имени исполнителя."""
    executor_country = message.text
    data = await state.get_data()

    user = UserSQLAlchemyRepository().get_user_by_telegram(
        telegram=message.chat.id,
    )
    executor = ExecutorSQLAlchemyRepository().get_executor_by_id(
        user_id=user.id,
        id=int(data["executor_id"]),
    )
    ExecutorSQLAlchemyRepository().update_country(
        execotor_country=executor_country,
        user_id=user.id,
        executor_id=executor.id,
    )
    AlbumSQLAlchemyRepository().update_executor_county_is_album(
        executor_id=executor.id,
        executor_country=executor_country,
    )

    await state.clear()
    await message.answer(
        "Страна исполнителя успешно изменена", reply_markup=ReplyKeyboardRemove()
    )
    await get_executors_information(message=message)


# Логика для удаления альбома
class DeleteAlbum(StatesGroup):
    """FSM для удаления альбома."""

    executor_id = State()
    album_id = State()


@router.callback_query(F.data.startswith("delete_album "))
async def start_delete_album(call: CallbackQuery, state: FSMContext):
    """Реакция на нажатие кнопки delete_album."""
    _, data = call.data.split(" ")
    executor_id, album_id = data.split("_")

    await state.clear()
    await state.set_state(DeleteAlbum.executor_id)
    await state.update_data(executor_id=int(executor_id))
    await state.set_state(DeleteAlbum.album_id)
    await state.update_data(album_id=int(album_id))

    await call.message.answer(
        "Вы уверены что хотите удалить этот альбом ? Наберите любой символ если хотите удалить альбом или нажмите 'Я передумал'",
        reply_markup=get_delete_executor_and_album_button(),
    )


@router.message(DeleteAlbum.album_id, F.text)
async def finish_delete_album(message: Message, state: FSMContext):
    """Работа с FSM DeleteAlbum.Удаляет альбом из музыкального архива."""
    data = await state.get_data()

    mess = message.text
    if mess == "Я передумал":
        await state.clear()
        await message.answer(
            "Удаление альбома отменено",
            reply_markup=ReplyKeyboardRemove(),
        )
        await get_executors_information(message=message)
    else:
        AlbumSQLAlchemyRepository().delete_album_is_id(
            executor_id=data["executor_id"],
            album_id=data["album_id"],
        )

        await state.clear()
        await message.answer("Альбом успешно удален")
        await get_executors_information(message=message)
