from . import Base
from uuid import UUID

from sqlalchemy import String, Text

from sqlalchemy.orm import Mapped, relationship, mapped_column


class Project(Base):
    __tablename__ = "projects"

    id: Mapped[UUID] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(32))
    description: Mapped[str] = mapped_column(String(500))
    price: Mapped[int]
    price_description: Mapped[str] = mapped_column(String(255))
    pdf_url: Mapped[str] = mapped_column(Text)

    images: Mapped[list["Image"]] = relationship(
        back_populates="project", cascade="all, delete-orphan"
    )
