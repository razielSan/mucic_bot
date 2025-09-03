from models.db_helper import db_helper
from models import GenreExecutor


class GenreExecutorSQLAlchemyRepository:
    """Репозиторий связующей модели жанра и исполнителя."""

    model: GenreExecutor

    def executor_genre(self, executor_id: int, genre_id: int):
        """Создает связь между жанром и исполнителем"""
        with db_helper.get_sesson() as session:
            try:
                genre_exeucotor = GenreExecutor(executor_id=executor_id, genre_id=genre_id)
                session.add(genre_exeucotor)
                session.commit()
            except Exception as err:
                print(err)
                session.rollback()

    def delete_executor_genre(self, executor_id: int):
        """Разрывает все связи с жанрами у исполнителя по executor_id."""
        with db_helper.get_sesson() as session:
            try:
                session.query(GenreExecutor).filter_by(executor_id=executor_id).delete()
                session.commit()
            except Exception as err:
                print(err)
                session.rollback()
