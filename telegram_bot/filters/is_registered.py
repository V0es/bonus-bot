from aiogram.filters import Filter
from aiogram.types import Message, CallbackQuery

from sqlalchemy.orm import sessionmaker

from db.requests import get_user_by_id

from exceptions import UserNotFoundException


class IsRegistered(Filter):
    def __init__(self, session_pool: sessionmaker) -> None:
        self.session_pool = session_pool

    async def __call__(self, event: Message | CallbackQuery) -> bool:

        async with self.session_pool() as session:
            try:
                if isinstance(event, Message):
                    await get_user_by_id(session, event.from_user.id)
                else:
                    await get_user_by_id(session, event.from_user.id)
                return True

            except UserNotFoundException:
                return False
