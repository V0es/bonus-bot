from telegram_bot.keyboards import (get_registered_start_keyboard as reg_start_kb,
                                    get_unregistered_start_keyboard as unreg_start_kb)


from aiogram import types, Router

router = Router()


@router.message()
async def start_unregistered(message: types.Message) -> None:
    """
    Handler for start command if user is not registered
    """
    await message.answer('Здравствуйте, кажется, вы не зарегистрированы в нашей системе.',
                         reply_markup=unreg_start_kb())


@router.message()
async def start_registered(message: types.Message) -> None:
    """
    Handler for start command if user not registered
    """
    await message.answer('Привет, я бот бонусной программы. Нажми кнопнку ниже, чтобы войти в главное меню.',
                         reply_markup=reg_start_kb())
