from __future__ import annotations
from typing import List

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, UniqueConstraint

from extensions import Base


class GenreExecutor(Base):
    """Связующая модель жанра и исполнителя."""

    __tablename__ = "genre_executor"

    executor_id: Mapped[int] = mapped_column(
        ForeignKey("executor.id"),
        primary_key=True,
    )
    genre_id: Mapped[int] = mapped_column(
        ForeignKey("genre.id"),
        primary_key=True,
    )


class Executor(Base):
    """Модель для исполнителя песен."""

    __tablename__ = "executor"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    country: Mapped[str]
    img: Mapped[str] = mapped_column(
        default="Здесь скоро появится изображение",
        server_default="Здесь скоро появится изображение",
    )

    user_id: Mapped[int] = mapped_column(
        ForeignKey(
            "user.id",
        )
    )
    user: Mapped["User"] = relationship(
        back_populates="executors",
    )

    albums: Mapped[List["Album"]] = relationship(
        back_populates="executor",
        cascade="all, delete",
        lazy="subquery",
    )
    genres: Mapped[List[Gengre]] = relationship(
        back_populates="executors",
        secondary="genre_executor",
        lazy="subquery",
    )

    __table_args__ = (
        UniqueConstraint(
            "name",
            "country",
            "user_id",
            name="name_country_userid_uc",
        ),
    )

    def __repr__(self):
        """Представление модели исполнителя."""
        return str(self.name)


class Gengre(Base):
    """Модель для жанра."""

    __tablename__ = "genre"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(unique=True)

    executors: Mapped[List[Executor]] = relationship(
        secondary="genre_executor",
        back_populates="genres",
        lazy="subquery",
        uselist=True,
    )

    def __repr__(self):
        """Представление модели жанра."""
        return str(self.title)
