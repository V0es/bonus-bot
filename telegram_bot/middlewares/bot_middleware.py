from typing import Callable, Dict, Any, Awaitable

from aiogram import BaseMiddleware, Bot
from aiogram.types import Message, TelegramObject, CallbackQuery

from db.requests import get_user_by_id


class BotMiddleware(BaseMiddleware):
    def __init__(self, bot: Bot) -> None:
        # super.__init__()
        self.bot = bot

    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any]
    ) -> Any:
        data['bot'] = self.bot
        return await handler(event, data)
