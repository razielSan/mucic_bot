from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

from config import settings


class DataBaseHeler:
    """Помощник для базы данных."""

    def __init__(self):
        self.engine = create_engine(url=settings.SQLITE_BASE)
        self.session_factory = sessionmaker(bind=self.engine)

    def get_sesson(self):
        with self.session_factory() as session:
            return session


db_helper = DataBaseHeler()
