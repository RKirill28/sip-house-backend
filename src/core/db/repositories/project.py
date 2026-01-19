from typing import Sequence

from sqlalchemy import func, select

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

    async def get_random(self, limit: int) -> Sequence[Project]:
        projects = await self.session.execute(
            select(Project).order_by(func.rand()).limit(limit)
        )
        return projects.scalars().all()
