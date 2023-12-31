from aiogram.filters import Filter
from aiogram.types import Message, CallbackQuery

from sqlalchemy.orm import sessionmaker

from telegram_bot.db.requests import is_owner

from telegram_bot.exceptions import UserNotFoundException


class IsOwner(Filter):
    def __init__(self, session_pool: sessionmaker) -> None:
        self.session_pool = session_pool

    async def __call__(self, event: Message | CallbackQuery) -> bool:
        async with self.session_pool() as session:
            try:
                return await is_owner(session, event.from_user.id)
            except UserNotFoundException:
                return False
