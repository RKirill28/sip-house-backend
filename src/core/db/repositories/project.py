from src.core.db.db_schemas import DBProjectModel
from src.core.db.repositories import BaseRepository
from src.core.db.models import Project


class ProjectRepository(BaseRepository[Project, DBProjectModel]):
    model = Project
