from typing import Callable, Dict, Any, Awaitable

from sqlalchemy.orm import sessionmaker

from aiogram import BaseMiddleware
from aiogram.types import Message, TelegramObject, CallbackQuery

from telegram_bot.db.requests import get_user_by_id


class DatabaseMiddleware(BaseMiddleware):
    def __init__(self, session_pool: sessionmaker) -> None:
        # super.__init__()
        self.session_pool = session_pool

    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: Message | CallbackQuery,
        data: Dict[str, Any]
    ) -> Any:
        async with self.session_pool() as session:
            data['session'] = session
            return await handler(event, data)
