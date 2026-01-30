from uuid import UUID
from fastapi import APIRouter, HTTPException, BackgroundTasks, Query

from src.core.db.repositories.base import NoEntityByIdFound
from src.core.schemas import (
    CreateMessageModel,
    ReadMessageModel,
    MessageModel,
)
from src.core.conifg import settings
from src.api.deps import MessageRepoDap
from src.api.deps import TelegramServiceDap


mess_router = APIRouter(prefix=settings.api.v1.messages_prefix)


@mess_router.post("", response_model=ReadMessageModel)
async def create(mess_repo: MessageRepoDap, create_mess: CreateMessageModel = Query()):
    new = await mess_repo.create(create_mess)
    return new


@mess_router.post("/send")
async def send(
    mess_repo: MessageRepoDap,
    tg_service: TelegramServiceDap,
    bg_tasks: BackgroundTasks,
    message_id: UUID = Query(),
):
    try:
        mess = await mess_repo.get_by_id(message_id)
        bg_tasks.add_task(
            tg_service.send_messages,
            message=MessageModel(
                username=mess.user_phone,
                user_phone=mess.user_phone,
                user_email=mess.user_email,
                comment=mess.comment,
                object_type=mess.object_type,
            ),
        )
    except NoEntityByIdFound:
        raise HTTPException(404, "No message found by id.")
