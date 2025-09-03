from typing import List

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import BigInteger

from models import Base


class User(Base):
    """Модель пользователя."""

    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    telegram: Mapped[int] = mapped_column(BigInteger, unique=True)

    executors: Mapped[List["Executor"]] = relationship(
        back_populates="user",
        uselist=True,
        lazy="subquery",
    )
