from keyboards import client_keyboard

from aiogram import types


async def login(callback: types.CallbackQuery):
    await callback.message.answer('Вы нажали кнопку ВОЙТИ', reply_markup=client_keyboard)
    await callback.answer()