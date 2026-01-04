from . import Base
from uuid import UUID, uuid4

from sqlalchemy import CHAR, String, Text, text

from sqlalchemy.orm import Mapped, relationship, mapped_column


class Project(Base):
    __tablename__ = "projects"

    name: Mapped[str] = mapped_column(String(32))
    description: Mapped[str] = mapped_column(String(500))
    price: Mapped[int]
    price_description: Mapped[str] = mapped_column(String(255))
    pdf_url: Mapped[str | None] = mapped_column(Text, default=None)

    images: Mapped[list["Image"]] = relationship(
        back_populates="project", cascade="all, delete-orphan"
    )
