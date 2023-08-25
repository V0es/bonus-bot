from aiogram.filters import Filter
from aiogram.types import Message, CallbackQuery

from sqlalchemy.orm import sessionmaker

from db.requests import is_admin

from exceptions import UserNotFoundException


class IsAdmin(Filter):

    def __init__(self, session_pool: sessionmaker) -> None:
        self.session_pool = session_pool

    async def __call__(self, event: Message | CallbackQuery) -> bool:
        # return True
        async with self.session_pool() as session:
            try:
                if isinstance(event, Message):

                    admin_flag = await is_admin(session, event.from_user.id)
                    return True if admin_flag else False

                else:

                    admin_flag = await is_admin(session, event.from_user.id)
                    return True if admin_flag else False
                
            except UserNotFoundException:
                return False
