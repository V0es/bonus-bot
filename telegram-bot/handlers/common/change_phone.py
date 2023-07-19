from aiogram import types

async def change_phone(message: types.Message):
    await message.answer(f"Phone changed!")