from aiogram import Router, F
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.filters import StateFilter

from repository.user import UserSQLAlchemyRepository
from repository.executor import ExecutorSQLAlchemyRepository
from functions import get_executors_is_users


router = Router(name=__name__)


@router.message(StateFilter(None), F.text == "🎸 Список исполнителей 🎸")
async def get_list_executors(message: Message):
    """Вывыдит список исполнителей которые есть у пользователя."""

    user = UserSQLAlchemyRepository().get_user_by_telegram(
        telegram=message.chat.id,
    )

    if not user:
        UserSQLAlchemyRepository().create_user(
            telegram=message.chat.id,
            name=message.from_user.first_name,
        )
        user = UserSQLAlchemyRepository().get_user_by_telegram(
            telegram=message.chat.id,
        )

    executor_list = ExecutorSQLAlchemyRepository().get_executors_is_user(
        user_id=user.id
    )
    if executor_list:
        data = get_executors_is_users(
            list_executor=executor_list,
            user=user,
        )
        await message.answer(
            f"{data}",
            reply_markup=ReplyKeyboardRemove(),
        )
    else:
        await message.answer("У вас нет исполнителей в музыкальном архиве")
