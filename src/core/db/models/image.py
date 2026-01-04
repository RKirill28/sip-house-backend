from typing import Optional
from .base import Base

from uuid import UUID, uuid4

from sqlalchemy import ForeignKey, String, Text
from sqlalchemy.orm import Mapped, relationship, mapped_column


class Image(Base):
    __tablename__ = "images"

    url: Mapped[str] = mapped_column(Text)
    name: Mapped[str] = mapped_column(String(32))
    description: Mapped[str] = mapped_column(String(255))
    is_main_image: Mapped[bool]
    sort: Mapped[int]

    project_id: Mapped[Optional[int]] = mapped_column(ForeignKey("projects.id"))
    project: Mapped[Optional["Project"]] = relationship(
        back_populates="images",
    )

    done_project_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("done_projects.id")
    )
    done_project: Mapped[Optional["DoneProject"]] = relationship(
        back_populates="images"
    )
