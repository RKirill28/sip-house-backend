from .base import Base

from sqlalchemy import ForeignKey, UUID, URL, String
from sqlalchemy.orm import Mapped, relationship, mapped_column


class Link(Base):
    __tablename__ = "images"

    id: Mapped[UUID] = mapped_column(primary_key=True)
    url: Mapped[URL]
    name: Mapped[str] = mapped_column(String(32))
    description: Mapped[str]
    is_main_image: bool
    sort: int

    project_id: Mapped[int] = mapped_column(ForeignKey("projects.id"))
    project: Mapped["Project"] = relationship(back_populates="images")
