from keyboards import start_keyboard


from aiogram import types, Router
from aiogram.filters import CommandStart

router = Router()


@router.message()
async def start(message: types.Message) -> None:
    await message.answer('Привет, я бот!', reply_markup=start_keyboard)
