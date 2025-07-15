from __future__ import annotations
from typing import List

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey

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
    """Модель для исплнителя песен."""

    __tablename__ = "executor"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=True)
    country: Mapped[str] = mapped_column(default="")

    user_id: Mapped[int] = mapped_column(
        ForeignKey(
            "user.id",
        )
    )
    user: Mapped["User"] = relationship(
        back_populates="executors",
    )

    songs: Mapped["Song"] = relationship(
        back_populates="executor",
        cascade="all, delete",
        lazy="subquery",
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


class Gengre(Base):
    """Модель для жанра."""
    __tablename__ = "genre"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(unique=True)

    executors: Mapped[List[Executor]] = relationship(
        secondary="genre_executor",
        back_populates="genres",
        lazy="subquery",
    )
