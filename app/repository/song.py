from typing import List

from models.db_helper import db_helper
from models import Song


class SongSQLAlchemyRepository:
    """Репозиторий для модели песни."""

    model: Song

    def create_songs(
        self,
        songs: List,
        album_id: int,
        executor_name: str,
        executor_album: str,
        order=None,
    ):
        """Создание песен для альбома."""
        with db_helper.get_sesson() as session:
            try:
                list_songs = []
                order = order if order else 1
                for index, songs in enumerate(songs, start=order):
                    list_songs.append(
                        Song(
                            order=index,
                            name=songs[1],
                            album_id=album_id,
                            file_id=songs[0],
                            executor_name=executor_name,
                            executor_album=executor_album,
                        )
                    )
                session.add_all(list_songs)
                session.commit()
                session.close()
                return True
            except Exception as err:
                session.rollback()
                print(err)
                return False

    def update_executor_name_is_song(
        self,
        list_albums_id: List,
        executor_name: str,
    ):
        """Обновляет execucotr_name у песен по album_id."""
        with db_helper.get_sesson() as session:
            try:
                session.query(Song).filter(Song.album_id.in_(list_albums_id)).update(
                    {Song.executor_name: executor_name}
                )
                session.commit()
            except Exception as err:
                print(err)
                session.rollback()
                return False

    def update_executor_album_is_song(
        self,
        album_id: int,
        executor_album: str,
    ):
        """Обновляет executor_album у песен.."""
        with db_helper.get_sesson() as session:
            try:
                session.query(Song).filter(Song.album_id == album_id).update(
                    {Song.executor_album: executor_album}
                )
                session.commit()
            except Exception as err:
                print(err)
                session.rollback()
                return False

    def get_songs(self, album_id: int):
        """Возвращает все песни из альбома по id."""
        with db_helper.get_sesson() as session:
            try:
                songs = (
                    session.query(Song)
                    .filter_by(album_id=album_id)
                    .order_by(Song.order)
                    .all()
                )
                return songs
            except Exception as err:
                session.rollback()
                print(err)
                return False

    def get_songs_by_order(
        self,
        album_id: int,
        order_songs: List,
    ):
        """Возвращает песни из альбома по номеру."""
        with db_helper.get_sesson() as session:
            try:
                songs = (
                    session.query(Song)
                    .filter(
                        Song.album_id == album_id,
                        Song.order.in_(order_songs),
                    )
                    .order_by(Song.order)
                    .all()
                )

                return songs
            except Exception as err:
                session.rollback()
                print(err)
                return False

    def get_song(self, name: str):
        """Возвращает одну песню из альбома по имени."""
        with db_helper.get_sesson() as session:
            try:
                songs = (
                    session.query(Song)
                    .filter_by(
                        name=name,
                    )
                    .first()
                )
                return songs
            except Exception as err:
                session.rollback()
                print(err)
                return False

    def delete_songs(self, album_id: int, order_songs: List[int]):
        """Удаляет песни из альбома."""
        with db_helper.get_sesson() as session:
            try:
                session.query(Song).filter(
                    Song.order.in_(order_songs),
                    Song.album_id == album_id,
                ).delete()
                session.commit()
                return True
            except Exception as err:
                session.rollback()
                print(err)
                return False

    def delete_all_songs(self, album_id: int):
        """Удаляет все песни из альбома."""
        with db_helper.get_sesson() as session:
            try:
                session.query(Song).filter(
                    Song.album_id == album_id,
                ).delete()
                session.commit()
                return True
            except Exception as err:
                session.rollback()
                print(err)
                return False
