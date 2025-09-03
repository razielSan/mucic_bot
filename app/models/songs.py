from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, UniqueConstraint

from extensions import Base


class Song(Base):
    """Модель песен исполнителя."""

    __tablename__ = "song"

    id: Mapped[int] = mapped_column(primary_key=True)
    order: Mapped[int]
    executor_name: Mapped[str] = mapped_column(default="Скоро здесь будет имя исполнителя")
    executor_album: Mapped[str] = mapped_column(default="Скоро здесь будет название альбома")
    name: Mapped[str]
    file_id: Mapped[str]

    album_id: Mapped[int] = mapped_column(ForeignKey("album.id", ondelete="CASCADE"))
    album: Mapped["Album"] = relationship(
        back_populates="songs",
        lazy="subquery",
    )

    __table_args__ = (
        UniqueConstraint(
            "name",
            "album_id",
            name="name_albumid_executorid_uc",
        ),
    )
