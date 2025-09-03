from sqlalchemy import text

from models.db_helper import db_helper
from models import Album


class AlbumSQLAlchemyRepository:
    """Репозиторий для модели альбома."""

    model = Album

    def create_album(
        self,
        title: str,
        year: int,
        executor_name: str,
        executor_id: int,
        executor_country: str,
        img="Здесь скоро появится изображение",
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
                    img=img,
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

    def get_albums(self, executor_id: int):
        """Возвращает список всех альбомов исполнителя по executor_id."""
        with db_helper.get_sesson() as session:
            album = (
                session.query(Album)
                .filter_by(
                    executor_id=executor_id,
                )
                .order_by(Album.year)
                .all()
            )
            session.close()
            return album

    def get_album_is_id(
        self,
        album_id: int,
        executor_id: int,
    ):
        """Возвращает альбом исполнителя по id."""
        with db_helper.get_sesson() as session:
            try:
                album = (
                    session.query(Album)
                    .filter_by(
                        executor_id=executor_id,
                        id=album_id,
                    )
                    .first()
                )
                session.close()
                return album
            except Exception as err:
                session.rollback()
                print(err)
                return False

    def delete_all_albums(self, executor_id: int):
        """Удаляет все альбомы исполнителя."""
        try:
            with db_helper.get_sesson() as session:
                session.execute(text("PRAGMA foreign_keys=ON"))
                session.query(Album).filter_by(executor_id=executor_id).delete()
                session.commit()
                session.close()
                return True
        except Exception as err:
            print(err)
            session.rollback()
            session.close()
            return False

    def update_executor_name_is_album(self, executor_id: int, executor_name: str):
        """Изменяет executor_name в альбоме."""
        with db_helper.get_sesson() as session:
            try:
                session.query(Album).filter(Album.executor_id == executor_id).update(
                    {
                        Album.executor_name: executor_name,
                    }
                )

                session.commit()
                return True
            except Exception as err:
                print(err)
                session.rollback()
                return False

    def update_executor_county_is_album(self, executor_id: int, executor_country: str):
        """Изменяет executor_country в альбоме."""
        with db_helper.get_sesson() as session:
            try:
                session.query(Album).filter(Album.executor_id == executor_id).update(
                    {
                        Album.executor_country: executor_country,
                    }
                )

                session.commit()
                return True
            except Exception as err:
                print(err)
                session.rollback()
                return False

    def update_title_is_album(
        self,
        executor_id: int,
        album_id: int,
        title: str,
    ):
        """Изменяет title в альбоме."""
        with db_helper.get_sesson() as session:
            try:
                session.query(Album).filter(
                    Album.executor_id == executor_id,
                    Album.id == album_id,
                ).update(
                    {
                        Album.title: title,
                    }
                )

                session.commit()
                return True
            except Exception as err:
                print(err)
                session.rollback()
                return False

    def delete_album(self, title: str, year: int, executor_id: int):
        """Удаляет альбом."""
        try:
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
        except Exception as err:
            print(err)
            session.rollback()
            return False

    def delete_album_is_id(
        self,
        executor_id: int,
        album_id: int,
    ):
        """Удаляет альбом по id."""
        try:
            with db_helper.get_sesson() as session:
                session.execute(text("PRAGMA foreign_keys=ON"))
                session.query(Album).filter_by(
                    id=album_id,
                    executor_id=executor_id,
                ).delete()
                session.commit()
                session.close()
                return True
        except Exception as err:
            print(err)
            session.rollback()
            return False
