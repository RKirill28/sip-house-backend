from src.core.db.repositories import BaseRepository
from src.core.db.models import DoneProject
from src.core.schemas import DoneProjectModel


class DoneProjectRepository(BaseRepository[DoneProject, DoneProjectModel]):
    model = DoneProject
