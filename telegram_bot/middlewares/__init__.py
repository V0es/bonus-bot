from aiogram import Router, Bot

from sqlalchemy.ext.asyncio import AsyncSession

from .database_middleware import DatabaseMiddleware
from .bot_middleware import BotMiddleware


def register_middlewares(router: Router, session_pool: AsyncSession, bot: Bot):
    router.message.middleware(DatabaseMiddleware(session_pool))
    router.callback_query.middleware(DatabaseMiddleware(session_pool))
    router.message.middleware(BotMiddleware(bot))
