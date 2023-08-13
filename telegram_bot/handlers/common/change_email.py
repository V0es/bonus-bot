from aiogram import types
from aiogram.fsm.context import FSMContext


async def change_email(callback: types.CallbackQuery, state):
    await message.answer("Email changed!")
