from aiogram import types

async def add_admin(message: types.Message):
    await message.answer(f"Admin added!")