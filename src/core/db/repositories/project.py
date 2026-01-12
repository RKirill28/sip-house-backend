from typing import Sequence

from sqlalchemy import func, select, desc
from src.core.enums import ProjectSortBy
from src.core.schemas import CreateProjectModel
from src.core.db.repositories import BaseRepository
from src.core.db.models import Project
from src.core.schemas.project import UpdateProjectModel


class ProjectRepository(BaseRepository[Project, CreateProjectModel]):
    model = Project

    async def update(self, update_model: UpdateProjectModel) -> Project:
        project = await self.session.get_one(Project, update_model.id)
        project.pdf_urls = update_model.pdf_urls
        return project

    async def get_all_with_count(
        self, offset: int, limit: int, sort_by: ProjectSortBy, is_desc: bool
    ) -> tuple[Sequence[Project], int]:
        print(sort_by.project_attr)
        if is_desc:
            sort_by_param = desc(sort_by.project_attr)
        else:
            sort_by_param = sort_by.project_attr
        res = await self.session.execute(
            select(self.model).order_by(sort_by_param).offset(offset).limit(limit)
        )
        count = await self.session.execute(select(Project.id))
        return (res.scalars().all(), len(count.scalars().all()))

    async def get_random(self, limit: int) -> Sequence[Project]:
        projects = await self.session.execute(
            select(Project).order_by(func.rand()).limit(limit)
        )
        return projects.scalars().all()
