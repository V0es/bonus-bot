import logging
import asyncio
from aioredis import Redis

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.redis import RedisStorage
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.enums import ParseMode
from aiogram.utils.token import TokenValidationError

from .config import config
from telegram_bot.handlers.common import register_common_handlers
from telegram_bot.handlers.client import register_client_handlers
from telegram_bot.handlers.admin import register_admin_handlers
from telegram_bot.handlers.admin.owner import register_owner_handlers
from telegram_bot.middlewares import register_middlewares

from .db.engine import get_session_pool, create_engine, proceed_schemas
from .db.base import BaseModel


async def main() -> None:
    # Get redis instance
    if config.bot_fsm_storage == 'memory':
        # Initialize memory storage
        storage = MemoryStorage()
    
    elif config.bot_fsm_storage == 'redis':
        redis = Redis(
            host=config.redis_host,
            port=config.redis_port,
            username=config.redis_username or None,
            password=config.redis_password or None
        )
        # Initialize redis storage
        storage = RedisStorage(redis=redis)
    else:
        logging.critical('FSM storage type is not specified or not supported')
        return
    # Initialize bot and dispatcher
    dp = Dispatcher(storage=storage)
    
    try:
        bot = Bot(token=config.bot_token, parse_mode=ParseMode.HTML)
    except TokenValidationError:
        logging.critical('Telegram bot token is invalid, unable to start bot')  # log message and return
        return

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
    logging.basicConfig(
        level=logging.INFO,
        filename='tg_bot.log',
        encoding='utf-8',
        format='%(asctime)s %(levelname)s %(message)s',
        datefmt='%d/%m/%Y %H:%M:%S')

    asyncio.run(main())
