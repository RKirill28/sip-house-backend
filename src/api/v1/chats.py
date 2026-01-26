from uuid import UUID
from fastapi import APIRouter, HTTPException, BackgroundTasks, Query

from src.core.db.repositories.base import NoEntityByIdFound
from src.core.schemas import (
    CreateMessageModel,
    ReadMessageModel,
    ChatModel,
    MessageModel,
    CreateChatModel,
)
from src.core.conifg import settings
from src.api.deps import ChatRepoDap, MessageRepoDap
from src.tg_bot.bot import send_messages


chats_router = APIRouter(prefix=settings.api.v1.messages_prefix)


# @chats_router.put('/update')
# async def update_chats(chat_repo: ChatRepoDap, model: CreateChatModel):
#     await chat_repo.
