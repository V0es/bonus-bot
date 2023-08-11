from typing import Callable, Dict, Any, Awaitable

from sqlalchemy.orm import sessionmaker

from aiogram import BaseMiddleware
from aiogram.types import Message, TelegramObject


class DatabaseMiddleware(BaseMiddleware):
    def __init__(self, session_pool: sessionmaker) -> None:
        # super.__init__()
        self.session_pool = session_pool

    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any]
    ) -> Any:
        async with self.session_pool() as session:
            print('DB MIDDLEWARE, SESSION: ', session)
            data['session'] = session
            return await handler(event, data)
