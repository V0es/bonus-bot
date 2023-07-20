from keyboards import start_keyboard


from aiogram import types

async def start(message: types.Message):
    await message.answer('Привет, я бот!', reply_markup=start_keyboard)