from uuid import UUID
from fastapi import APIRouter, HTTPException, BackgroundTasks, Query

from src.core.db.repositories.base import NoEntityByIdFound
from src.core.schemas import (
    CreateMessageModel,
    ReadMessageModel,
    ChatModel,
    CreateChatModel,
    MessageModel,
)
from src.core.conifg import settings
from src.api.deps import ChatRepoDap, MessageRepoDap
from src.tg_bot.bot import send_messages


mess_router = APIRouter(prefix=settings.api.v1.messages_prefix)


@mess_router.post("", response_model=ReadMessageModel)
async def create(mess_repo: MessageRepoDap, create_mess: CreateMessageModel = Query()):
    new = await mess_repo.create(create_mess)
    return new


@mess_router.post("/send")
async def send(
    mess_repo: MessageRepoDap,
    chat_repo: ChatRepoDap,
    bg_tasks: BackgroundTasks,
    message_id: UUID = Query(),
):
    try:
        chats = await chat_repo.get_chats()
        for chat in chats:
            if not await chat_repo.get_by_chat_id(chat.chat_id):
                await chat_repo.create(
                    CreateChatModel(chat_id=chat.chat_id, username=chat.username)
                )

        mess = await mess_repo.get_by_id(message_id)
        bg_tasks.add_task(
            send_messages,
            MessageModel(
                username=mess.user_phone,
                user_phone=mess.user_phone,
                user_email=mess.user_email,
                comment=mess.comment,
                object_type=mess.object_type,
            ),
            [ChatModel(chat_id=chat.chat_id, username=chat.username) for chat in chats],
        )

    except NoEntityByIdFound:
        raise HTTPException(404, "No message found by id.")
