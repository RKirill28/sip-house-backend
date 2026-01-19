from src.core.db.repositories import BaseRepository
from src.core.db.models import DoneProject
from src.core.sort_by_enums import DoneProjectSortBy
from src.core.schemas import CreateDoneProjectModel


class DoneProjectRepository(
    BaseRepository[DoneProject, CreateDoneProjectModel, DoneProjectSortBy]
):
    model = DoneProject
