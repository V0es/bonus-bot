import logging

from aiogram import Bot, Dispatcher, executor, types

from config import bot_token

logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=bot_token)
dp = Dispatcher(bot)

from handlers import register_handlers
register_handlers(dp)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)