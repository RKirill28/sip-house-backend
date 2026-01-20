from telegram import Bot

from src.core.schemas import (
    CreateChatModel,
    MessageModel,
    ChatModel,
)
from src.core.conifg import settings

import asyncio


bot = Bot(token=settings.TG_BOT_TOKEN)


async def get_chats() -> list[CreateChatModel]:
    upds = await bot.get_updates()
    chats = []

    for upd in upds:
        chat = upd.effective_chat
        if chat:
            chats.append(CreateChatModel(chat_id=chat.id, username=chat.username))
    return chats


async def send_messages(message: MessageModel, chats: list[ChatModel]) -> None:
    _message = f"""
📞 Phone: {message.user_phone}

📧 E-mail: {message.user_email}

🏠 Object type: <i>{message.object_type.value}</i>

💬 Comment: <b>{message.comment}</b>
    """

    for chat in chats:
        await bot.send_message(chat.chat_id, _message, parse_mode="html")


if __name__ == "__main__":
    asyncio.run(get_chats())
