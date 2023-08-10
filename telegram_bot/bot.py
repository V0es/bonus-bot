import logging
import asyncio

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.enums import ParseMode

from config import bot_token
from handlers.common import register_common_commands
# from handlers import register_handlers

logging.basicConfig(level=logging.INFO)


async def main() -> None:
    storage = MemoryStorage()  # switch to Redis or Mongo
    # Initialize bot and dispatcher
    dp = Dispatcher(storage=storage)
    bot = Bot(token=bot_token, parse_mode=ParseMode.HTML)
    await bot.delete_webhook(drop_pending_updates=True)
    register_common_commands(dp)
    await dp.start_polling(bot)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
