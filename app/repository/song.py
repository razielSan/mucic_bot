from typing import List

from sqlalchemy import text

from models.db_helper import db_helper
from models import Song


class SongSQLAlchemyRepository:
    model: Song

    def create_songs(
        self,
        order: int,
        song: str,
        album_id: int,
        executor_id: int,
        file_id: str,
    ):
        with db_helper.get_sesson() as session:
            list_songs = []
            for order, song in enumerate(songs, start=order):
                list_songs.append(
                    Song(
                        order=order,
                        name=song,
                        album_id=album_id,
                        executor_id=executor_id,
                        file_id=file_id,
                    )
                )
            session.add_all(list_songs)
            session.commit()
            return True
