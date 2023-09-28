import logging

from aiogram import Router, Bot

from sqlalchemy.orm import sessionmaker

from .database_middleware import DatabaseMiddleware
from .bot_middleware import BotMiddleware


def register_middlewares(router: Router, session_pool: sessionmaker, bot: Bot):
    router.message.middleware(DatabaseMiddleware(session_pool))
    router.callback_query.middleware(DatabaseMiddleware(session_pool))
    router.message.middleware(BotMiddleware(bot))
    logging.info('Middlewares registered')
