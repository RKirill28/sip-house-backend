from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session

from src.core.conifg import settings
from src.core.db.models import Base, Admin
from src.services.hasher import Hasher


sync_mysql_url = settings.db.sync_url.unicode_string()
sync_engine = create_engine(sync_mysql_url, echo=True)


def create_all():
    Base.metadata.create_all(bind=sync_engine)
    with Session(sync_engine) as session:
        admin = session.execute(
            select(Admin).where(Admin.username == settings.admin_username)
        ).scalar_one_or_none()

        password = Hasher.hash_password(settings.admin_pass)
        if admin:
            admin.password = password
            admin.username = settings.admin_username
        else:
            admin = Admin(username="admin", password=password)
            session.add(admin)
        session.commit()


if __name__ == "__main__":
    create_all()
