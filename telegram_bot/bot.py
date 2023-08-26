import logging
import asyncio

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.redis import RedisStorage
from aiogram.enums import ParseMode
from aiogram.utils.token import TokenValidationError

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from aioredis import Redis

from middlewares.database_middleware import DatabaseMiddleware
from middlewares.bot_middleware import BotMiddleware

from config import config
from handlers.common import register_common_handlers
from handlers.client import register_client_handlers
from handlers.admin import register_admin_handlers
from handlers.admin.owner import register_owner_handlers
from middlewares import register_middlewares
# from handlers import register_handlers

from db.engine import get_session_pool, create_engine, proceed_schemas
from db.base import BaseModel


logging.basicConfig(level=logging.DEBUG)


async def main() -> None:
    redis = Redis(
        host=config.redis_host,
        port=config.redis_port,
        username=config.redis_username or None,
        password=config.redis_password or None
    )
    
    storage = RedisStorage(redis=redis)  # switch to Redis or Mongo
    # Initialize bot and dispatcher
    dp = Dispatcher(storage=storage)
    
    try:
        bot = Bot(token=config.bot_token, parse_mode=ParseMode.HTML)
    except TokenValidationError:
        pass
    
    await bot.delete_webhook(drop_pending_updates=True)
    
    engine = create_engine(config.db_url)
    session_pool = get_session_pool(engine)
   
    await proceed_schemas(session_pool, BaseModel.metadata, engine, config.debug)

    register_middlewares(dp, session_pool, bot)
    register_common_handlers(dp, session_pool)
    register_client_handlers(dp, session_pool)
    register_admin_handlers(dp, session_pool)
    register_owner_handlers(dp, session_pool)
    
    await dp.start_polling(bot)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
