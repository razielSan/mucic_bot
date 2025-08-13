from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from extensions import bot
from keyboards.inline import (
    get_search_inline_button,
    get_button_is_search_executor,
    get_albums_executors_button,
)
from keyboards.reply import get_search_reply_button, get_music_menu_button
from repository.user import UserSQLAlchemyRepository
from repository.executor import ExecutorSQLAlchemyRepository
from repository.album import AlbumSQLAlchemyRepository
from repository.song import SongSQLAlchemyRepository
from functions import get_info_executors


router = Router(name=__name__)


@router.message(F.text == "🔎 Поиск 🔍")
async def search(message: Message):
    """Возвращает инлайн клавиатуру поиска для пользователя."""
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

    for index, executor in enumerate(executors):
        if executor.name == user.name and executor.country == user.name:
            executors.pop(index)

    if not executors:
        await message.answer(
            "У вас нет исполнителей в музыкальном архиве",
            reply_markup=get_music_menu_button(),
        )
        return

    await bot.delete_message(
        chat_id=message.chat.id,
        message_id=message.message_id,
    )

    await message.answer(
        "Выберито то из списка что хотите найти", reply_markup=ReplyKeyboardRemove()
    )
    await bot.send_message(
        text="Варианты поиска",
        chat_id=message.chat.id,
        reply_markup=get_search_inline_button(),
    )


# Логика для поиска по имени, стране и жанру
class SearchName(StatesGroup):
    """FSM для поиска по имени, стране и жанру."""

    executor_name = State()
    executor_country = State()
    ececutor_genre = State()


@router.callback_query(F.data.startswith("search_country"))
@router.callback_query(F.data.startswith("search_genre"))
@router.callback_query(F.data.startswith("search_name"))
@router.callback_query(F.data.startswith("search_all"))
async def search_name(call: CallbackQuery, state: FSMContext):
    """Возвращает пользователю сообщение с просьбой написать имя исполнителя."""
    await state.clear()

    _, search = call.data.split("_")
    if search.startswith("name"):
        search = "имя"
        await state.set_state(SearchName.executor_name)
        await state.update_data(executor_name=True)
    elif search == "country":
        search = "страну"
        await state.set_state(SearchName.executor_country)
        await state.update_data(executor_country=True)
    elif search == "genre":
        search = "жанр"
        await state.set_state(SearchName.ececutor_genre)
        await state.update_data(genre=True)
    else:
        user = UserSQLAlchemyRepository().get_user_by_telegram(
            telegram=call.message.chat.id,
        )
        executors = ExecutorSQLAlchemyRepository().get_executors_is_user(
            user_id=user.id,
        )

        await state.clear()
        await bot.send_message(
            chat_id=call.message.chat.id,
            text="Поиск завершен",
            reply_markup=ReplyKeyboardRemove(),
        )

        # Удаляет из выдачи всех исполнителей сборник песен
        for index, executor in enumerate(executors):
            if executor.name == user.name and executor.country == user.name:
                executors.pop(index)

        await call.message.answer(
            text="Список найденных исполнителей",
            reply_markup=get_button_is_search_executor(
                executors_list=executors,
            ),
        )
        return

    await call.message.answer(
        text=f"Напишите {search} исполнителя которого хотите найти или нажмите 'Отмена'",
        reply_markup=get_search_reply_button(),
    )


@router.message(SearchName.executor_name, F.text)
@router.message(SearchName.executor_country, F.text)
@router.message(SearchName.ececutor_genre, F.text)
async def search_executor(message: Message, state: FSMContext):
    """Возвращает список исполнителей по имени, стране и жанру."""
    data = await state.get_data()
    executor_name = data.get("executor_name")
    executor_country = data.get("executor_country")
    genre = data.get("genre")

    mess = message.text
    if mess == "Отмена":
        await state.clear()
        await message.answer(
            "Поиск исполнителя отменен", reply_markup=ReplyKeyboardRemove()
        )
        await search(message=message)
    else:
        user = UserSQLAlchemyRepository().get_user_by_telegram(telegram=message.chat.id)
        if executor_name:

            executors_list = ExecutorSQLAlchemyRepository().get_executors_is_user(
                user_id=user.id
            )
            executors = []
            for executor in executors_list:
                if executor.name.lower() == mess.lower():
                    executors.append(executor)
            await state.clear()
            await bot.send_message(
                chat_id=message.chat.id,
                text="Поиск завершен",
                reply_markup=ReplyKeyboardRemove(),
            )
            if not executors:
                await message.answer("Такого исполнителя нет в музыкальном архиве")
                await search(message=message)
            else:
                await message.answer(
                    text="Список найденных исполнителей",
                    reply_markup=get_button_is_search_executor(
                        executors_list=executors,
                    ),
                )
        elif executor_country:
            executors_list = ExecutorSQLAlchemyRepository().get_executors_is_user(
                user_id=user.id
            )
            executors = []
            for executor in executors_list:
                if executor.country.lower() == mess.lower():
                    executors.append(executor)

            await state.clear()
            await bot.send_message(
                chat_id=message.chat.id,
                text="Поиск завершен",
                reply_markup=ReplyKeyboardRemove(),
            )
            if not executors:
                await message.answer(
                    "C такой страной нет исполнителя в музыкальном архиве"
                )
                await search(message=message)
            else:
                await message.answer(
                    text="Список найденных исполнителей",
                    reply_markup=get_button_is_search_executor(
                        executors_list=executors,
                    ),
                )
        elif genre:
            executors = ExecutorSQLAlchemyRepository().get_executors_is_user(
                user_id=user.id
            )
            list_executors = []
            for executor in executors:
                for g in executor.genres:
                    if g.title.lower() == mess.lower():
                        list_executors.append(executor)
            await state.clear()
            await bot.send_message(
                chat_id=message.chat.id,
                text="Поиск завершен",
                reply_markup=ReplyKeyboardRemove(),
            )

            if not list_executors:
                await message.answer(
                    "В таком жанре нет исполнителей в музыкальном архиве"
                )
                await search(message=message)
            else:
                await message.answer(
                    text="Список найденных исполнителей",
                    reply_markup=get_button_is_search_executor(
                        executors_list=list_executors,
                    ),
                )


@router.callback_query(F.data.startswith("input "))
async def show_executors_is_search(call: CallbackQuery):
    """Возвращает исполнителя найденного по поиску."""
    _, executor_id = call.data.split(" ")

    user = UserSQLAlchemyRepository().get_user_by_telegram(
        telegram=call.message.chat.id,
    )
    executor = ExecutorSQLAlchemyRepository().get_executor_by_id(
        id=int(executor_id), user_id=user.id
    )

    data_executor = get_info_executors(executor=executor, user=user)

    album = None
    list_songs = None

    await bot.send_message(
        chat_id=call.message.chat.id,
        reply_markup=ReplyKeyboardRemove(),
        text="Список Исполнителей",
    )
    await call.message.answer(
        text=data_executor,
        reply_markup=get_albums_executors_button(
            executor=executor,
            user=user,
            album=album,
            list_songs=list_songs,
        ),
    )
