from typing import List

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, UniqueConstraint

from extensions import Base


class Album(Base):
    """Модель альбома."""

    __tablename__ = "album"

    id: Mapped[int] = mapped_column(primary_key=True)
    executor_name: Mapped[str]
    executor_country: Mapped[str] = mapped_column(
        default="Скоро здесь будет название страны"
    )
    title: Mapped[str]
    year: Mapped[int]
    img: Mapped[str] = mapped_column(
        default="Здесь скоро появится изображение",
        server_default="Здесь скоро появится изображение",
    )

    executor_id: Mapped[int] = mapped_column(
        ForeignKey("executor.id", ondelete="CASCADE")
    )
    executor: Mapped["Executor"] = relationship(
        back_populates="albums", lazy="subquery"
    )
    songs: Mapped[List["Song"]] = relationship(
        back_populates="album",
        lazy="subquery",
    )

    __table_args__ = (
        UniqueConstraint(
            "executor_name",
            "title",
            "executor_id",
            name="executorname_title_executorid_uc",
        ),
    )
