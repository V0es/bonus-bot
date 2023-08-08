from aiogram import types

async def add_order(message: types.Message):
    amount = int(int(message.text.split(' ')[1]) * 5 / 100) # parse message with regex
    await message.answer(f'You have earned {amount} bonus points!')
