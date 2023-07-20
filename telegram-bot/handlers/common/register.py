from aiogram import types

# register state with FSM
async def register(callback: types.CallbackQuery):
    await callback.message.answer('U pressed Register')
    await callback.answer()