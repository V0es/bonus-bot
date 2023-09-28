from aiogram.filters import Filter
from aiogram.types import Message, CallbackQuery

from sqlalchemy.orm import sessionmaker

from telegram_bot.db.requests import is_admin

from telegram_bot.exceptions import UserNotFoundException


class IsAdmin(Filter):

    def __init__(self, session_pool: sessionmaker) -> None:
        self.session_pool = session_pool

    async def __call__(self, event: Message | CallbackQuery) -> bool:
        # return True
        async with self.session_pool() as session:
            try:
                return await is_admin(session, event.from_user.id)
            except UserNotFoundException:
                return False
