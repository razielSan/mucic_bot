from typing import List
from urllib.parse import quote

import requests
from bs4 import BeautifulSoup

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

        album = "\n\n🎧 Список альбомов 🎧"

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
        "Искать музыку в интернете - Возвращает меню из доступных опций поиска\n\n"
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


def get_found_list_artists_for_hitmotop(url: str, name: str, count: int):
    """Ищет музыку исполнителя с сайта https://ru.hitmotop.com и возвращает
    список с url для скачивания.

    Args:
        url (str): URL для поиска исполнителя
        name (str): Имя исполнителя
        count (int): Количество треков
    """

    name = quote(string=f"{name}")

    url = f"https://ru.hitmotop.com/search?q={name}"

    HEADERS = {
        "Accept": "*/*",
        "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Mobile Safari/537.36",
    }

    response = requests.get(url=url, headers=HEADERS)

    soup = BeautifulSoup(response.text, "lxml")

    artists = soup.find_all(
        name="li",
        attrs={"class": "tracks__item track mustoggler"},
    )

    list_artists = []
    for index, music in enumerate(artists):
        if index >= count:
            break
        array = music.get("data-musmeta")
        data = eval(array)
        artist = data["artist"]
        title = data["title"]
        url = data["url"].replace("\\", "")
        list_artists.append([artist, title, url])

    return list_artists


def get_data_names_and_title_aritists(list_artists: List):
    """Возвращает строку содержащую имя исполнителя и название песни в формате
    1. <executor_name> - <title>

    Args:
        list_artists (List): Список состоящий из имени артиста, название песни и url для скачивания в формате
        [<artists>, <title>, <url>]
    """

    data_list = []
    order = 1
    for executor, title, url in list_artists:
        data_list.append(f"{order}. {executor} - {title}")
        order += 1
    return "\n".join(data_list).strip("\\n")


def download_music_to_the_path(url: str, path: str):
    """_summary_

    Args:
        url (str): _description_
        path (str): _description_
        filename (str): _description_
    """
    HEADERS = {
        "Accept": "*/*",
        "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Mobile Safari/537.36",
    }

    res = requests.get(url, headers=HEADERS, stream=True)
    with open(f"{path}", "wb") as file:
        for chunk in res.iter_content(1024):
            file.write(chunk)
