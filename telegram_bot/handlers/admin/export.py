from aiogram import types

async def export(message: types.Message):
    await message.answer(f"Exported!")