from .base import Base

from uuid import UUID, uuid4

from sqlalchemy import ForeignKey, String, Text
from sqlalchemy.orm import Mapped, relationship, mapped_column


class Image(Base):
    __tablename__ = "images"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    url: Mapped[str] = mapped_column(Text)
    name: Mapped[str] = mapped_column(String(32))
    description: Mapped[str] = mapped_column(String(255))
    is_main_image: Mapped[bool]
    sort: Mapped[int]

    project_id: Mapped[int] = mapped_column(ForeignKey("projects.id"))
    project: Mapped["Project"] = relationship(back_populates="images")
