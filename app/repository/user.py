from models.db_helper import db_helper

from models import User


class UserSQLAlchemyRepository:
    """Репозиторий для модели пользователя."""

    model = User

    def create_user(self, telegram: int, name: str):
        with db_helper.get_sesson() as session:
            try:
                user = User(
                    name=name,
                    telegram=telegram,
                )
                session.add(user)
                session.commit()
                return True
            except Exception as err:
                session.rollback()
                session.close()
                print(err)
                return False

    def get_user_by_telegram(self, telegram: int):
        with db_helper.get_sesson() as session:
            try:
                user = session.query(User).filter_by(telegram=telegram).first()
                session.close()
                return user
            except Exception as err:
                session.rollback()
                print(err)
                return False
