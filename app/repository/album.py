from sqlalchemy import text

from models.db_helper import db_helper
from models import Album, Executor


class AlbumSQLAlchemyRepository:
    model = Album

    def create_album(
        self,
        title: str,
        year: int,
        executor_name: str,
        executor_id: int,
        executor_country: str,
    ):
        """Создание альбома для исполнителя."""
        with db_helper.get_sesson() as session:
            try:
                album = Album(
                    title=title,
                    year=year,
                    executor_name=executor_name,
                    executor_id=executor_id,
                    executor_country=executor_country,
                )
                session.add(album)
                session.commit()
                session.close()
                return True
            except Exception as err:
                print(err)
                session.rollback()
                return False

    def get_album(self, executor_name: str, title: str, executor_id: int):
        """Возвращает альбом исполнителя."""
        with db_helper.get_sesson() as session:
            album = (
                session.query(Album)
                .filter_by(
                    executor_id=executor_id,
                    title=title,
                    executor_name=executor_name,
                )
                .first()
            )
            session.close()
            return album

    def delete_album(self, title: str, year: int, executor_id: int):
        """Удаляет альбом."""
        with db_helper.get_sesson() as session:
            session.execute(text("PRAGMA foreign_keys=ON"))
            session.query(Album).filter_by(
                title=title,
                year=year,
                executor_id=executor_id,
            ).delete()
            session.commit()
            session.close()
            return True
