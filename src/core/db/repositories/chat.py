from src.core.db.models import Chat
from src.core.sort_by_enums import ChatSortBy
from src.core.schemas import CreateChatModel

from typing import Sequence
from sqlalchemy import select

from . import BaseRepository


class ChatRepository(BaseRepository[Chat, CreateChatModel, ChatSortBy]):
    model = Chat

    async def get_chats(self) -> Sequence[Chat]:
        res = await self.session.execute(select(self.model))
        return res.scalars().all()

    async def get_chat_ids(self) -> Sequence[int]:
        res = await self.session.execute(select(self.model.chat_id))
        return res.scalars().all()

    async def get_by_chat_id(self, chat_id: int) -> Chat | None:
        res = await self.session.execute(select(Chat).where(Chat.chat_id == chat_id))
        return res.scalar()
