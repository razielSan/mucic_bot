from sqlalchemy import text

from models.db_helper import db_helper
from models import Album, Executor


class AlbumSQLAlchemyRepository:
    model = Album

    def create_album(self, title: str, year: int, executor: Executor):
        with db_helper.get_sesson() as session:
            try:
                album = Album(
                    title=title,
                    year=year,
                    executor_name=executor.name,
                )
                album.executor = executor
                session.add(album)
                session.commit()
                return True
            except Exception as err:
                print(err)
                session.rollback()
                return False

    def get_album(self, executor: Executor, title: str, year: int):
        with db_helper.get_sesson() as session:
            album = (
                session.query(Album)
                .filter_by(executor_id=executor.id, title=title, year=year)
                .first()
            )
            return album

    def delete_album(self, title: str, year: int, executor_id: int):
        with db_helper.get_sesson() as session:
            session.execute(text("PRAGMA foreign_keys=ON"))
            session.query(Album).filter_by(
                title=title,
                year=year,
                executor_id=executor_id,
            ).delete()
            session.commit()
            return True
