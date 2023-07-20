import logging

from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from config import bot_token

logging.basicConfig(level=logging.INFO)

storage = MemoryStorage() # switch to Redis or Mongo


# Initialize bot and dispatcher
bot = Bot(token=bot_token)
dp = Dispatcher(bot, storage=storage)


from handlers import register_handlers
register_handlers(dp)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)