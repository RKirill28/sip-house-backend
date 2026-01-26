from typing import AsyncGenerator

from sqlalchemy.exc import IntegrityError
from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from src.core.conifg import settings
from src.core.db.models import Base, Admin
from src.services.hasher import Hasher


# WARN:if remove this imports then all crashed and tables will not create


sqlite_file_name = "database.db"
async_mysql_url = settings.db.async_url.unicode_string()
sync_mysql_url = settings.db.sync_url.unicode_string()

async_engine = create_async_engine(async_mysql_url, echo=True)
sync_engine = create_engine(sync_mysql_url, echo=True)

AsyncSessionMaker = async_sessionmaker(
    async_engine, expire_on_commit=False, autoflush=False
)


def create_all():
    # with sync_engine.begin() as _: # autocommited if no errors
    Base.metadata.create_all(bind=sync_engine)
    with Session(sync_engine) as session:
        admin = session.execute(
            select(Admin).where(Admin.username == settings.admin_pass)
        ).scalar_one_or_none()

        password = Hasher.hash_password(settings.admin_pass)
        if admin:
            admin.password = password
        else:
            admin = Admin(username="admin", password=password)
            session.add(admin)

        session.commit()


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionMaker() as session:
        try:
            yield session
            await session.commit()
        except:
            await session.rollback()
            raise
