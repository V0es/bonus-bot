from aiogram import types

async def login(message: types.Message):
    await message.answer(f"Logged in!")