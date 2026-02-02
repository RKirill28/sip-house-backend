from fastapi import APIRouter

from src.core.schemas import ReadChatModel
from src.core.conifg import settings

from src.api.deps import TelegramServiceDap

chats_router = APIRouter(prefix=settings.api.v1.chats_prefix)


@chats_router.put("", response_model=list[ReadChatModel])
async def update_chats(tg_service: TelegramServiceDap):
    return await tg_service.update_chat_list()
