from src.core.db.repositories import BaseRepository
from src.core.db.models import DoneProject


class DoneProjectRepository(BaseRepository[DoneProject, DoneProjectModel]):
    model = DoneProject
