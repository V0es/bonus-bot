from aiogram import types

async def change_email(message: types.Message):
    await message.answer(f"Email changed!")