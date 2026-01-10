from typing import Sequence, override

from sqlalchemy import select
from sqlalchemy.orm import selectinload
from src.core.schemas import CreateProjectModel
from src.core.db.repositories import BaseRepository
from src.core.db.models import Project
from src.core.schemas.project import UpdateProjectModel


class ProjectRepository(BaseRepository[Project, CreateProjectModel]):
    model = Project

    @override
    async def get_all(self) -> Sequence[Project]:
        res = await self.session.execute(
            select(self.model).options(selectinload(Project.images))
        )
        return res.scalars().all()

    async def update(self, update_model: UpdateProjectModel) -> Project:
        project = await self.session.get_one(Project, update_model.id)
        project.pdf_urls = update_model.pdf_urls
        return project
