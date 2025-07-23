from typing import List

from models.db_helper import db_helper
from models import Gengre


class GengreSQLAlchemyRepository:
    """Репозиторий для модели жанра."""

    model = Gengre

    def create_one_genre(self, title: str):
        """Создание одного жанра."""
        with db_helper.get_sesson() as session:
            try:
                genre = Gengre(
                    title=title,
                )
                session.add(genre)
                session.commit()
                session.close()
                return True
            except Exception as err:
                session.rollback()
                session.close()
                print(err)
                return False

    def create_many_genre(self, title_list: List):
        """Создание множества жанров."""
        with db_helper.get_sesson() as session:
            try:
                for title in title_list:
                    genre = Gengre(
                        title=title,
                    )
                    session.add(genre)
                session.commit()
                session.close()
                return True
            except Exception as err:
                session.rollback()
                session.close()
                print(err)
                return False

    def get_genres(self, title_list: List):
        """Возвращает список жанров если они есть в модели Genre."""
        with db_helper.get_sesson() as session:
            try:
                genre = session.query(Gengre).filter(Gengre.title.in_(title_list)).all()
                session.close()
                return genre
            except Exception as err:
                session.rollback()
                session.close()
                print(err)
                return False

    def get_all_genre(self):
        """Возвращает список всех жанров."""
        with db_helper.get_sesson() as session:
            try:
                genre_set = session.query(Gengre).all()
                if genre_set:
                    session.close()
                    return {genre.title for genre in genre_set}
                session.close()
                return genre_set
            except Exception as err:
                session.rollback()
                session.close()
                print(err)
                return False
