from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey

from extensions import Base


class Song(Base):
    """Модель песен исполнителя."""

    __tablename__ = "song"

    id: Mapped[int] = mapped_column(primary_key=True)
    order: Mapped[int]
    name: Mapped[str]
    file_id: Mapped[str]

    album_id: Mapped[int] = mapped_column(ForeignKey("album.id", ondelete="CASCADE"))
    album: Mapped["Album"] = relationship(
        back_populates="songs",
        lazy="subquery",
    )
    executor_id: Mapped[int] = mapped_column(
        ForeignKey("executor.id", ondelete="CASCADE")
    )
    executor: Mapped["Executor"] = relationship(
        back_populates="songs",
        lazy="subquery",
    )
