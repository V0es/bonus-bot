from aiogram import types


async def set_account(message: types.Message):
    new_bouns = message.text.split(' ')[1]
    await message.answer(f'Your account is set to {new_bouns} bonus points!')