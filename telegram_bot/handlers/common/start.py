from keyboards import (get_registered_start_keyboard as reg_start_kb,
                       get_unregistered_start_keyboard as unreg_start_kb)

from states import UserState

from aiogram import types, Router
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext

router = Router()


@router.message()
async def start_unregistered(message: types.Message) -> None:
    await message.answer('Здравствуйте, кажется, вы не зарегистрированы в нашей системе.', reply_markup=unreg_start_kb())


@router.message()
async def start_registered(message: types.Message, state: FSMContext) -> None:
    await message.answer('Привет, я бот бонусной программы. Нажми кнопнку ниже, чтобы войти в главное меню.', reply_markup=reg_start_kb())
