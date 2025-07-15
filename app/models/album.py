from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, UniqueConstraint

from extensions import Base


class Album(Base):
    """Модель альбома."""

    __tablename__ = "album"

    id: Mapped[int] = mapped_column(primary_key=True)
    executor_name: Mapped[str]
    title: Mapped[str]
    year: Mapped[int]

    executor_id: Mapped[int] = mapped_column(
        ForeignKey("executor.id", ondelete="CASCADE")
    )
    executor: Mapped["Executor"] = relationship(
        back_populates="albums", lazy="subquery"
    )
    songs: Mapped["Song"] = relationship(back_populates="album", lazy="subquery")

    __table_args__ = (
        UniqueConstraint(
            "executor_name",
            "title",
            name="executorname_title_uc",
        ),
    )
