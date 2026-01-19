from src.core.sort_by_enums import MessageSortBy
from src.core.schemas import CreateMessageModel
from src.core.db.models import Message

from . import BaseRepository


class MessageRepository(BaseRepository[Message, CreateMessageModel, MessageSortBy]):
    model = Message
