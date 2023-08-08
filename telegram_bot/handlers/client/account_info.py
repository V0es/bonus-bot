from aiogram import types

async def account_info(callback: types.CallbackQuery):
    await callback.message.answer(f"You have something on balance.")
    await callback.answer()