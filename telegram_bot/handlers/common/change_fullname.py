from aiogram import Router, types
from aiogram.fsm.context import FSMContext

from sqlalchemy.ext.asyncio import AsyncSession

from telegram_bot.states import UserState

from telegram_bot.utils.validators import validate_fullname

from telegram_bot.exceptions import UserNotFoundException

from telegram_bot.db.requests import change_fullname as change_user_fullname

from telegram_bot.keyboards import get_back_to_main_menu_keyboard as back_to_mainmenu_kb


router = Router()


@router.callback_query()
async def change_fullname(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.edit_text('Введите новое имя')
    await state.set_state(UserState.change_fullname)


@router.message()
async def enter_new_fullname(message: types.Message, state: FSMContext, session: AsyncSession):
    answer = message.text
    if not validate_fullname(answer):
        await message.answer('Вы ввели некорректное имя, попробуйте ещё раз', reply_markup=back_to_mainmenu_kb())
        return
    else:
        try:
            await change_user_fullname(session, message.from_user.id, answer)
            await message.answer('Имя успешно изменено!', reply_markup=back_to_mainmenu_kb())
        except UserNotFoundException:
            await message.answer('Произошёл сбой. Попробуйте позже', reply_markup=back_to_mainmenu_kb())
            await state.clear()
            return
        
