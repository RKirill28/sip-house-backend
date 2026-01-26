from src.core.sort_by_enums import ProjectSortBy
from src.core.schemas import (
    CreateProjectModel,
    UpdateProjectPdfUrlModel,
)
from src.core.db.repositories import BaseRepository
from src.core.db.models import Project


class ProjectRepository(BaseRepository[Project, CreateProjectModel, ProjectSortBy]):
    model = Project

    async def update_pdf_url(self, update_model: UpdateProjectPdfUrlModel) -> Project:
        project = await self.get_by_id(update_model.id)
        project.pdf_urls = update_model.pdf_urls
        return project
