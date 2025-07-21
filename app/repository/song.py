from typing import List

from sqlalchemy import text

from models.db_helper import db_helper
from models import Song


class SongSQLAlchemyRepository:
    model: Song

    def create_songs(
        self,
        songs: List,
        album_id: int,
        executor_name: str,
        executor_album: str,
    ):
        """Создание песен для альбома."""
        with db_helper.get_sesson() as session:
            try:
                list_songs = []
                for order, songs in enumerate(songs, start=1):
                    list_songs.append(
                        Song(
                            order=order,
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
