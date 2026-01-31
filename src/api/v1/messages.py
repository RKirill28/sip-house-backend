from uuid import UUID
from fastapi import APIRouter, HTTPException, Query

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
    message_id: UUID = Query(),
):
    try:
        mess = await mess_repo.get_by_id(message_id)
        await tg_service.send_messages(
            MessageModel(
                user_name=mess.user_phone,
                user_phone=mess.user_phone,
                user_email=mess.user_email,
                comment=mess.comment,
                object_type=mess.object_type,
            )
        )
        return {"success": True}
    except NoEntityByIdFound:
        raise HTTPException(404, "No message found by id.")
