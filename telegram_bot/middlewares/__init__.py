from aiogram import Router

from sqlalchemy.ext.asyncio import AsyncSession

from .database_middleware import DatabaseMiddleware


def register_middlewares(router: Router, session_pool: AsyncSession):
    router.message.middleware(DatabaseMiddleware(session_pool))
    router.callback_query.middleware(DatabaseMiddleware(session_pool))
