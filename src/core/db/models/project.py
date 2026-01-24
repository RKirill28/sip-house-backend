from . import Base

from sqlalchemy import String, Text, DECIMAL, JSON
from sqlalchemy.orm import Mapped, relationship, mapped_column


class Project(Base):
    __tablename__ = "projects"

    name: Mapped[str] = mapped_column(String(32))
    description: Mapped[str] = mapped_column(String(500))
    price: Mapped[float] = mapped_column(DECIMAL(10, 2))
    price_description: Mapped[str] = mapped_column(String(255))
    pdf_urls: Mapped[list[str] | None] = mapped_column(JSON, default=None)
    public: Mapped[bool] = mapped_column(default=False)

    images: Mapped[list["Image"]] = relationship(
        back_populates="project",
        cascade="all, delete-orphan",
        lazy="selectin",
    )
