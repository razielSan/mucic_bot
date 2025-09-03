from typing import List

from sqlalchemy import text, func

from models.db_helper import db_helper
from models import Executor, User


class ExecutorSQLAlchemyRepository:
    """Репозиторий для модели исполнителя."""

    model = Executor

    def create_executor(
        self,
        name: str,
        user: User,
        list_genres: List,
        country: str,
    ):
        """Создание исполнителя."""
        with db_helper.get_sesson() as session:
            try:
                executor = Executor(
                    name=name,
                    user_id=user.id,
                    country=country,
                )
                executor.genres.extend(list_genres)
                session.add(executor)
                session.commit()
                session.close()
                return True
            except Exception as err:
                session.rollback()
                session.close()
                print(err)
                return False

    def get_executor_by_name_and_country(
        self,
        name: str,
        user_id: int,
        country: str,
    ):
        """Возвращает исполнителя по имени и стране."""
        with db_helper.get_sesson() as session:
            try:
                executor = (
                    session.query(Executor)
                    .filter_by(
                        name=name,
                        user_id=user_id,
                        country=country,
                    )
                    .first()
                )
                session.close()
                return executor
            except Exception as err:
                session.rollback()
                session.close()
                print(err)
                return False

    def get_executors_by_name(
        self,
        name: str,
        user_id: int,
    ):
        """Возвращает исполнителей по имени."""
        with db_helper.get_sesson() as session:
            try:
                executor = (
                    session.query(Executor)
                    .filter_by(
                        name=name,
                        user_id=user_id,
                    )
                    .order_by(Executor.country)
                    .all()
                )
                session.close()
                return executor
            except Exception as err:
                session.rollback()
                session.close()
                print(err)
                return False

    def get_executors_by_country(
        self,
        country: str,
        user_id: int,
    ):
        """Возвращает исполнителей по стране."""
        with db_helper.get_sesson() as session:
            try:
                executor = (
                    session.query(Executor)
                    .filter_by(
                        country=country,
                        user_id=user_id,
                    )
                    .order_by(Executor.name)
                    .all()
                )
                session.close()
                return executor
            except Exception as err:
                session.rollback()
                session.close()
                print(err)
                return False

    def get_executor_by_id(self, id: int, user_id: int):
        """Возвращает исполнителя по id."""
        with db_helper.get_sesson() as session:
            try:
                executor = (
                    session.query(Executor)
                    .filter_by(
                        id=id,
                        user_id=user_id,
                    )
                    .first()
                )
                return executor
            except Exception as err:
                session.rollback()
                print(err)
                return False

    def get_executors_is_user(self, user_id: int):
        """Возвращает всех исполнителей которые есть у пользователя."""
        with db_helper.get_sesson() as session:
            try:
                executors = (
                    session.query(Executor)
                    .filter(Executor.user_id == user_id)
                    .order_by(
                        func.lower(Executor.name),
                    )
                ).all()
                return executors
            except Exception as err:
                session.rollback()
                print(err)
                return False

    def update_genre(
        self,
        executor_id: int,
        user_id: int,
        list_genres: List,
    ):
        """Изменяет жанры исполнителя."""
        with db_helper.get_sesson() as session:
            try:
                executor = (
                    session.query(Executor)
                    .filter_by(
                        id=executor_id,
                        user_id=user_id,
                    )
                    .first()
                )
                executor.genres = list_genres
                session.commit()
                return True
            except Exception as err:
                print(err)
                session.rollback()
                return False

    def resets_genres(
        self,
        executor_id: int,
        user_id: int,
    ):
        """Обнуляет жанры исполнителя."""
        with db_helper.get_sesson() as session:
            try:
                executor = (
                    session.query(Executor)
                    .filter_by(
                        id=executor_id,
                        user_id=user_id,
                    )
                    .first()
                )
                executor.genres = []
                session.commit()
                session.close()
                return True
            except Exception as err:
                print(err)
                session.rollback()
                session.close()
                return False

    def update_name(self, executor_id: int, user_id: int, execotor_name: str):
        """Обновляет имя исполнителя."""
        with db_helper.get_sesson() as session:
            try:
                executor = (
                    session.query(Executor)
                    .filter_by(id=executor_id, user_id=user_id)
                    .first()
                )
                executor.name = execotor_name
                session.commit()
                return True
            except Exception as err:
                print(err)
                session.close()
                return False

    def update_country(self, executor_id: int, user_id: int, execotor_country: str):
        """Обновляет страну исполнителя."""
        with db_helper.get_sesson() as session:
            try:
                executor = (
                    session.query(Executor)
                    .filter_by(id=executor_id, user_id=user_id)
                    .first()
                )
                executor.country = execotor_country
                session.commit()
                return True
            except Exception as err:
                print(err)
                session.close()
                return False

    def delete_executor_is_id(
        self,
        user_id: int,
        executor_id: int,
    ):
        """Удаление исполнителя по id."""
        try:
            with db_helper.get_sesson() as session:
                session.execute(text("PRAGMA foreign_keys=ON"))
                executor = (
                    session.query(Executor)
                    .filter_by(id=executor_id, user_id=user_id)
                    .first()
                )
                executor.genres = []
                session.delete(executor)
                session.commit()
                session.close()
                return True
        except Exception as err:
            print(err)
            session.rollback()
            session.close()
            return False

    def delete_executor(
        self,
        name: str,
        user_id: int,
        country: str,
    ):
        """Удаление исполнителя."""
        with db_helper.get_sesson() as session:
            try:
                session.execute(text("PRAGMA foreign_keys=ON"))

                executor = (
                    session.query(Executor)
                    .filter_by(
                        name=name,
                        user_id=user_id,
                        country=country,
                    )
                    .first()
                )
                executor.genres = []
                session.delete(executor)
                session.commit()
                session.close()
                return True
            except Exception as err:
                print(err)
                session.rollback()
                return False
