from models import Executor, User

from repository.executor import ExecutorSQLAlchemyRepository
from repository.genre import GengreSQLAlchemyRepository


def get_info_executors(executor: Executor):
    """Возвращает информацию о исполнителе."""
    data_list = []

    executors = [genre.title for genre in executor.genres]
    data = (
        f"🎧 {executor.name} 🎧\n\n🎧 Страна: {executor.country} 🎧\nЖанры: {executors[0]}"
    )
    data_list.append(data)
    data_list.extend(executors[1:])
    data_executor = ", ".join(data_list).strip(",")

    album = f"\n\n🎧 Список альбомов 🎧"

    info = "".join([data_executor, album])

    return info


def get_executor_is_button(
    executor_id: int,
    user: User,
    forward=False,
    back=False,
):
    """Возвращает исполнителя при нажатии на кнопку вперед или назад."""
    executor = ExecutorSQLAlchemyRepository().get_executor_by_id(
        id=executor_id,
        user_id=user.id,
    )

    executors_list = ExecutorSQLAlchemyRepository().get_executors_is_user(
        user_id=user.id,
    )

    order = 0
    for index, ex in enumerate(executors_list, start=1):
        if executor.name == ex.name and ex.country == executor.country:
            order = index
    if len(executors_list) == 1:
        order = 0
        return executors_list[order]
    else:
        order = order + 1 if forward else order - 1
    return executors_list[order - 1]
