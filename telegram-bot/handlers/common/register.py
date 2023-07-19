from aiogram import types

# register state with FSM
async def register(message: types.Message):
    await message.answer(f'You are registered!')