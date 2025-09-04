import os

from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove
from aiogram.filters import StateFilter

from extensions import bot
from keyboards.reply import get_add_music_button, get_music_menu_button
from keyboards.inline import get_button_is_collection_song
from error_handlers import cheak_data_is_number
from repository.executor import ExecutorSQLAlchemyRepository
from repository.album import AlbumSQLAlchemyRepository
from repository.song import SongSQLAlchemyRepository
from repository.user import UserSQLAlchemyRepository
from config import settings
from functions import get_info_executors
from views.add_collection_of_songs import start_add_collection_song


router = Router(name=__name__)


@router.message(StateFilter(None), F.text == f"🎶 {settings.AlBUM_TITLE_COLLECTION} 🎶")
async def get_collection_songs(message: Message):
    """Показывает пользователю сборник песен."""

    user = UserSQLAlchemyRepository().get_user_by_telegram(
        telegram=message.chat.id,
    )

    if not user:
        UserSQLAlchemyRepository().create_user(
            telegram=message.chat.id,
            name=message.from_user.first_name,
        )
        user = UserSQLAlchemyRepository().get_user_by_telegram(telegram=message.chat.id)

    executor = ExecutorSQLAlchemyRepository().get_executor_by_name_and_country(
        name=user.name, country=user.name, user_id=user.id
    )
    if executor:
        album = AlbumSQLAlchemyRepository().get_album(
            executor_name=executor.name,
            title=settings.AlBUM_TITLE_COLLECTION,
            executor_id=executor.id,
        )

        data_executor = get_info_executors(executor=executor, user=user)
        list_songs = SongSQLAlchemyRepository().get_songs(
            album_id=album.id,
        )

        await message.answer(
            text=data_executor,
            reply_markup=get_button_is_collection_song(
                songs_list=list_songs,
                executor=executor,
                album=album,
            ),
        )

    else:
        await message.answer("У вас еще нет сборника песен")


@router.callback_query(
    F.data.startswith("forward_songs ") | F.data.startswith("back_songs ")
)
async def get_collection_song_when_you_press_the_button(call: CallbackQuery):
    """Возвращает информацию о сборнике песен при нажатии кнопок назад или вперед."""
    button, data = call.data.split(" ")
    executor_id, album_id, order = data.split("_")
    forward = True if button.startswith("forward_songs") else False
    back = True if button.startswith("back_songs") else False

    user = UserSQLAlchemyRepository().get_user_by_telegram(
        telegram=call.message.chat.id,
    )
    executor = ExecutorSQLAlchemyRepository().get_executor_by_name_and_country(
        name=user.name, country=user.name, user_id=user.id
    )

    album = AlbumSQLAlchemyRepository().get_album(
        executor_name=executor.name,
        title=settings.AlBUM_TITLE_COLLECTION,
        executor_id=executor.id,
    )

    data_executor = get_info_executors(executor=executor, user=user)
    list_songs = SongSQLAlchemyRepository().get_songs(
        album_id=album.id,
    )

    order = int(order)
    await bot.edit_message_text(
        text=data_executor,
        reply_markup=get_button_is_collection_song(
            songs_list=list_songs,
            album=album,
            executor=executor,
            forward=forward,
            back=back,
            order=order,
        ),
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
    )


@router.callback_query(F.data.startswith("add_songs "))
async def handler_add_songs(call: CallbackQuery, state: FSMContext):
    """Перенаправляет на start_add_collection_song для добавления песен."""
    await start_add_collection_song(message=call.message, state=state)


# Логика для удаения песен
class DeleteSongsCollectionSong(StatesGroup):
    """FSM для удаления песен из сборника."""

    song = State()


@router.callback_query(F.data.startswith("delete_songs "))
async def handler_delete_songs(call: CallbackQuery, state: FSMContext):
    """Просит пользователя ввести номера песен для удаления."""

    await state.clear()
    await call.message.answer(
        "Нажмите 'Все' если хотите удалить все песни илии введите номера песен"
        "которые хотите удалить в формате\n\n1.2.5.10\n\nНажмите 'Отмена' для отмены удаления песен",
        reply_markup=get_add_music_button(all_song=True),
    )
    await state.set_state(DeleteSongsCollectionSong.song)


@router.message(DeleteSongsCollectionSong.song, F.text == "Отмена")
async def cancel_delete_songs_handler(message: Message, state: FSMContext):
    """Работа с FSM DeleteSongsCollectionSong.Отменяет все действия."""
    current_state = await state.get_state()

    if current_state is None:
        return

    await state.clear()
    await message.answer("Удаление песен из сборника отменено")
    await bot.send_message(
        chat_id=message.chat.id,
        text="Музыкальный архив",
        reply_markup=get_music_menu_button(),
    )


@router.message(DeleteSongsCollectionSong.song, F.text)
async def finish_delete_songs(message: Message, state: FSMContext):
    """Работа с FSM DeleteSongsCollectionSong. Удаляет выбранные пользователем песни."""
    all_song = False
    if message.text == "Все":
        all_song = True
    else:
        number_songs = message.text.split(".")
        list_number_songs = []
        for song in number_songs:
            result, mess = cheak_data_is_number(song, quantity=9_999_999_999)
            if not result:
                await message.answer(
                    f"{mess['error']}\n\nВведите снова номера песен которые"
                    "хотите удалить в формате\n\n1.2.5.10"
                )
                return
            list_number_songs.append(song)

    user = UserSQLAlchemyRepository().get_user_by_telegram(
        telegram=message.chat.id,
    )

    executor = ExecutorSQLAlchemyRepository().get_executor_by_name_and_country(
        name=user.name,
        country=user.name,
        user_id=user.id,
    )

    album = AlbumSQLAlchemyRepository().get_album(
        executor_name=executor.name,
        title=settings.AlBUM_TITLE_COLLECTION,
        executor_id=executor.id,
    )

    if all_song:
        # Удаляет песни из пути media/hitmotop/<user_name>/
        songs_delete_list = SongSQLAlchemyRepository().get_songs(album_id=album.id)
        for song in songs_delete_list:
            if song.file_id.find(settings.HITMOTOP_PATH) != -1:
                os.remove(song.file_id)
        SongSQLAlchemyRepository().delete_all_songs(album_id=album.id)

    else:
        songs_list = SongSQLAlchemyRepository().get_songs_by_order(
            album_id=album.id,
            order_songs=list_number_songs,
        )
        for song in songs_list:
            if song.file_id.find(settings.HITMOTOP_PATH) != -1:
                os.remove(song.file_id)

        SongSQLAlchemyRepository().delete_songs(
            album_id=album.id,
            order_songs=list_number_songs,
        )

        # Удаляет песни из пути media/hitmotop/<user_name>/
    await state.clear()
    await message.answer(
        "Песни были успешно удалены",
        reply_markup=ReplyKeyboardRemove(),
    )
    await get_collection_songs(message=message)
