from core.db.models import Base

from sqlalchemy import UUID, String
from sqlalchemy.orm import Mapped, relationship, mapped_column


class Project(Base):
    __tablename__ = "projcets"

    id: Mapped[UUID] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(32))
    description: Mapped[str]
    price: int
    price_description: str
    pdf_url: str

    images: Mapped[list["Image"]] = relationship(
        back_populates="project", cascade="all, delete-orphan"
    )
