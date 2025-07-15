from typing import List

from models.db_helper import db_helper
from models import Gengre


class GengreSQLAlchemyRepository:
    model = Gengre

    def create_genre(self, title: str):
        with db_helper.get_sesson() as session:
            try:
                genre = Gengre(
                    title=title,
                )
                session.add(genre)
                session.commit()
                return True
            except Exception as err:
                session.rollback()
                print(err)
                return False

    def get_genre(self, title_list: List):
        with db_helper.get_sesson() as session:
            try:
                genre = session.query(Gengre).filter(Gengre.title.in_(title_list)).all()
                return genre
            except Exception as err:
                session.rollback()
                print(err)
                return False

    def get_all_genre(self):
        with db_helper.get_sesson() as session:
            try:
                genre = session.query(Gengre).all()
                return genre
            except Exception as err:
                session.rollback()
                print(err)
                return False
