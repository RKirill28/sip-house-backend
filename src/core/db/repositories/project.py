from src.core.schemas import ProjectModel
from src.core.db.repositories import BaseRepository
from src.core.db.models import Project


class ProjectRepository(BaseRepository[Project, ProjectModel]):
    model = Project
