from core.db.models import Base

from uuid import UUID


class Project(Base):
    __tablename__ = "projcets"

    id: Mapped[UUID] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(32), unique=True, index=True)
    password: Mapped[str] = mapped_column(String(32))
    refresh_token: Mapped[UUID | None] = mapped_column(unique=True, default=None)
    expires_token: Mapped[datetime | None] = mapped_column(default=None)

    links: Mapped[list["Link"]] = relationship(
        back_populates="author", cascade="all, delete-orphan"
    )
