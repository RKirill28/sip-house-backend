from . import Base
from uuid import UUID, uuid4

from sqlalchemy import String, Text

from sqlalchemy.orm import Mapped, relationship, mapped_column


class DoneProject(Base):
    __tablename__ = "done_projects"

    name: Mapped[str] = mapped_column(String(32))
    address: Mapped[str] = mapped_column(String(32))

    images: Mapped[list["Image"]] = relationship(
        back_populates="done_project", cascade="all, delete-orphan"
    )
