from telegram import Bot

from src.core.conifg import settings
from src.core.db.repositories import ChatRepository
from src.core.schemas import CreateChatModel, MessageModel
from src.core.db.models import Chat


class TelegramService:
    """
    Умеет обновлять список чатов в бд и отправлять им уведомление об новой заявке.
    """

    _instance = None
    _bot = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        if cls._bot is None:
            cls._bot = Bot(settings.TG_BOT_TOKEN)
        return cls._instance

    def __init__(self, chat_repo: ChatRepository):
        self._chat_repo = chat_repo

    async def _get_chats(self) -> set[CreateChatModel]:
        updates = await self._bot.get_updates()
        chats = set()
        upd_chats = [upd.effective_chat for upd in updates]

        for upd in upd_chats:
            if upd:
                chats.add(CreateChatModel(chat_id=upd.id, username=upd.username))
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
        """
        Обновляет список чатов, если есть новые пользовтаеля бота
        """
        new_chats = await self._get_new_chats()
        res = await self._chat_repo.create_all(new_chats)
        await self._chat_repo.session.commit()
        return res

    async def send_messages(self, message: MessageModel) -> None:
        """
        Отправляет сообщения во все чаты из БД.
        """
        chats = await self._chat_repo.get_chats()
        _message = f"""
📞 Телефон: {message.user_phone}

📧 Почта: {message.user_email}

🏠 Тип объекта: <i>{message.object_type.value}</i>

💬 Комментарий: {message.comment}
        """
        for chat in chats:
            try:
                await self._bot.send_message(chat.chat_id, _message, parse_mode="html")
            except Exception as e:
                pass
