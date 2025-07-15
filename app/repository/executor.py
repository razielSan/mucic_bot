from typing import List

from sqlalchemy import text

from models.db_helper import db_helper
from models import Executor, User


class ExecutorSQLAlchemyRepository:
    model = Executor

    def create_executor(self, name: str, user: User, list_genres: List):
        with db_helper.get_sesson() as session:
            try:
                executor = Executor(
                    name=name,
                    user_id=user.id,
                )
                print("Hello")
                print(list_genres)
                executor.genres.extend(list_genres)
                session.add(executor)
                session.commit()
                return True
            except Exception as err:
                session.rollback()
                print(err)
                return False

    def get_executor_by_name(self, name: str, user_id: int):
        with db_helper.get_sesson() as session:
            try:
                executor = (
                    session.query(Executor)
                    .filter_by(
                        name=name,
                        user_id=user_id,
                    )
                    .first()
                )
                return executor
            except Exception as err:
                session.rollback()
                print(err)
                return False

    def delete_executor(self, name: str, user_id: int):
        with db_helper.get_sesson() as session:
            session.execute(text("PRAGMA foreign_keys=ON"))

            executor = (
                session.query(Executor).filter_by(name=name, user_id=user_id).first()
            )
            executor.genres = []
            session.delete(executor)
            session.commit()
            return True

            # except Exception as err:
            #     print(err)
            #     session.rollback()
            #     return False
