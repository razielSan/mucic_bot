from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from aiogram.filters import StateFilter

from functions import get_dict_executors_music_archive
from config import settings
from keyboards.inline import get_button_by_genre_executors_music_archive


router = Router(name=__name__)


@router.message(StateFilter(None), F.text == "💻 Список исполнителей музыкального хранилища 💻")
async def executors_music_archive_handler(message: Message):
    """Возвращает пользователю список жанров из музыкального хранилища."""
    executors = get_dict_executors_music_archive(
        path=settings.UPLOAD_PATH_MUSIC_ACRHIVE,
    )
    if executors:
        await message.answer(
            text="Выберите нужный жанр",
            reply_markup=get_button_by_genre_executors_music_archive(data=executors),
        )
    else:
        await message.answer("Произошла ошибка при доступе к музыкальному хранилищу")


@router.callback_query(F.data.startswith("genreMA_"))
async def get_executors_by_genre_music_archive(call: CallbackQuery):
    """Возвращает пользователю всех исполнителей по уканазому жанру
    из музыкального хранилища.
    """

    _, genre = call.data.split("_")
    executors = get_dict_executors_music_archive(
        path=settings.UPLOAD_PATH_MUSIC_ACRHIVE,
    )

    data = executors.get(genre)
    data.sort()
    for digit in range(0, len(data), 150):
        await call.message.answer("\n".join(data[digit : digit + 150]))
