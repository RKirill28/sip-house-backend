from .base import Base

from uuid import uuid4, UUID
from typing import Optional

from sqlalchemy import ForeignKey, String, Text
from sqlalchemy.orm import Mapped, relationship, mapped_column

from src.core.db.models.base import MyUUID


class Image(Base):
    __tablename__ = "images"

    url: Mapped[Optional[str]] = mapped_column(Text, default=None)
    name: Mapped[str] = mapped_column(String(32))
    description: Mapped[str] = mapped_column(String(255))
    main_image: Mapped[bool]
    sort: Mapped[int]

    project_id: Mapped[Optional[UUID]] = mapped_column(
        MyUUID, ForeignKey("projects.id"), default=None
    )
    project: Mapped[Optional["Project"]] = relationship(
        back_populates="images",
    )

    done_project_id: Mapped[Optional[UUID]] = mapped_column(
        MyUUID, ForeignKey("done_projects.id"), default=None
    )
    done_project: Mapped[Optional["DoneProject"]] = relationship(
        back_populates="images"
    )
