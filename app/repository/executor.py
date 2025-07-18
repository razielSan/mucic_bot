from typing import List

from sqlalchemy import text

from models.db_helper import db_helper
from models import Executor, User


class ExecutorSQLAlchemyRepository:
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
