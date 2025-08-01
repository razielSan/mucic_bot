from typing import List

from models import Executor, User
from repository.executor import ExecutorSQLAlchemyRepository


def get_info_executors(executor: Executor, user: User):
    """Возвращает информацию о исполнителе."""
    data_list = []

    if executor.country == user.name and executor.name == user.name:
        info = "🎧 Сборник песен  🎧"
    else:
        executors = [genre.title for genre in executor.genres]
        data = f"🎧 {executor.name} 🎧\n\n🎧 Страна: {executor.country} 🎧\nЖанры: {executors[0]}"
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


def get_info_is_bot():
    """Возвращает описание умений бота."""

    data = (
        "Описание умений бота\n\n\start - Возвращает главное меню бота\n\n"
        "Добавить музыку (самостоятельно) - Здесь вы добавляете музыку в музыкальный архив\n\n"
        "Добавить музыку (искать в сети) - Здесь вы ищете музыку в интернете\n\n"
        "Добавить музыку в сборник песен - Здесь вы можете сформировать свой сборник для отдельных песен\n\n"
        "Сборник песен - Выводит песни из сборника песен.Можете прослушивать их,удалять песни, добавлять песни\n\n"
        "Музыкальный архив - Выводит исполнителей в алфавитном порядке."
        "Здесь вы можете прослушивать музыку и совершать все действия по редактированию исполнителей."
        "Если нет исполнителей функция недоступна\n\n"
        "Список исполнителей - Выводит на экран всех исполнителей которые у вас есть\n\n"
        "Поиск - Здесь вы можете отыскать исполнителя по жанру, имени, стране или вывести всех исполнителей сразу."
        "Если нет исполнителей функция недоступна"
    )
    return data


def get_list_albums_executors(list_albums: List[str]):
    """Возвращает строку со всеми альбомами исполнителя."""
    albums = []
    for index, data in enumerate(list_albums, start=1):
        albums.append(f"{index}. {data}")
    return "\n".join(albums)


def get_executors_is_users(
    list_executor: List[Executor],
    user: User,
):
    """Возвращает список всех исполнителей которые есть у пользователя."""
    for index, executor in enumerate(list_executor):
        if executor.name == user.name and executor.country == user.name:
            list_executor.pop(index)
    data = [executor.name for executor in list_executor]

    data.sort()
    if data:
        executors = "\n".join(data)
    else:
        executors = "У вас нет исполнителей в музыкальном архиве"
    return executors
