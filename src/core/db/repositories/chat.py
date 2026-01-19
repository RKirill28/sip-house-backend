from src.core.db.models import Chat
from src.core.sort_by_enums import ChatSortBy
from src.core.schemas import CreateChatModel

from . import BaseRepository


class ChatRepository(BaseRepository[Chat, CreateChatModel, ChatSortBy]):
    model = Chat
