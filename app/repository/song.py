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
