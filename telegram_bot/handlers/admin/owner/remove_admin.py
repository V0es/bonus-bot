from aiogram import types

async def remove_admin(message: types.Message):
    await message.answer(f"Admin removed!")