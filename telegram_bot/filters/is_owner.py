from aiogram.filters import Filter
from aiogram.types import Message, CallbackQuery

from sqlalchemy.orm import sessionmaker

from db.requests import is_owner

from exceptions import UserNotFoundException


class IsOwner(Filter):
    def __init__(self, session_pool: sessionmaker) -> None:
        self.session_pool = session_pool

    async def __call__(self, event: Message | CallbackQuery) -> bool:
        async with self.session_pool() as session:
            try:
                if isinstance(event, Message):
                    return await is_owner(session, event.from_user.id)
                else:
                    return await is_owner(session, event.message.from_user.id)

            except UserNotFoundException:
                return False
