from aiogram import types

async def account_info(message: types.Message):
    await message.answer(f"You have something on balance.")