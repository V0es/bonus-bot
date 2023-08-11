import logging
import asyncio

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.enums import ParseMode

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from middlewares.database_middleware import DatabaseMiddleware

from config import config
from handlers.common import register_common_commands
from middlewares import register_middlewares
# from handlers import register_handlers

from db.engine import get_session_pool, create_engine, proceed_schemas
from db.base import BaseModel


logging.basicConfig(level=logging.INFO)


async def main() -> None:
    storage = MemoryStorage()  # switch to Redis or Mongo
    # Initialize bot and dispatcher
    dp = Dispatcher(storage=storage)
    bot = Bot(token=config.bot_token, parse_mode=ParseMode.HTML)
    await bot.delete_webhook(drop_pending_updates=True)
    
    engine = create_engine(config.db_url)
    session_pool = get_session_pool(engine)
   
    await proceed_schemas(session_pool, BaseModel.metadata, engine, config.debug)

    register_middlewares(dp, session_pool)
    register_common_commands(dp)
    await dp.start_polling(bot)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
