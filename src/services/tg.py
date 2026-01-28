from telegram import Bot

from src.core.conifg import settings
from src.core.db.models.chat import Chat
from src.core.db.repositories import ChatRepository
from src.core.schemas import CreateChatModel
from src.core.schemas.message import CreateMessageModel, ReadMessageModel


class TelegramService:
    """
    Умеет обновлять список чатов в бд и отправлять им уведомление об новой заявке.
    """

    _instance = None

    def __init__(self, chat_repo: ChatRepository):
        self._bot = Bot(settings.TG_BOT_TOKEN)
        self._chat_repo = chat_repo

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(TelegramService, cls).__new__(cls)
        return cls._instance

    async def _get_chats(self) -> list[CreateChatModel]:
        upds = await self._bot.get_updates()
        chats = []

        for upd in upds:
            chat = upd.effective_chat
            if chat:
                chats.append(CreateChatModel(chat_id=chat.id, username=chat.username))
        return chats

    async def _get_new_chats(self) -> list[CreateChatModel]:
        chat_ids_from_db = await self._chat_repo.get_chat_ids()
        chats_from_tg = await self._get_chats()

        new_chats = []
        for chat in chats_from_tg:
            if chat.chat_id not in chat_ids_from_db:
                new_chats.append(chat)
        return new_chats

    async def update_chat_list(self) -> list[Chat]:
        new_chats = await self._get_new_chats()
        return await self._chat_repo.add_all(new_chats)

    async def send_messages(self, message: CreateMessageModel) -> None:
        """
        Отпровляет сообщения во все чаты из БД.
        """
        chats = await self._chat_repo.get_chats()
        _message = f"""
📞 Телефон: {message.user_phone}

📧 Почта: {message.user_email}

🏠 Тип объекта: <i>{message.object_type.value}</i>

💬 Комментарий: {message.comment}
        """
        for chat in chats:
            await self._bot.send_message(chat.chat_id, _message, parse_mode="html")
