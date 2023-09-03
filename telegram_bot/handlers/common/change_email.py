from aiogram import types, Router
from aiogram.fsm.context import FSMContext

from sqlalchemy.ext.asyncio import AsyncSession

from telegram_bot.exceptions import UserNotFoundException

from telegram_bot.states import UserState, Register

from telegram_bot.db.requests import get_user_by_id

from telegram_bot.utils.otp import generate_otp
from telegram_bot.utils.validators import validate_email
from telegram_bot.utils.web import sms_auth

from telegram_bot.keyboards import get_back_to_main_menu_keyboard as back_to_mainmenu_kb

router = Router()


@router.callback_query()
async def change_email(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(UserState.change_email)
    await callback.message.edit_text('Введите новый email')


@router.message()
async def enter_new_email(message: types.Message, state: FSMContext, session: AsyncSession):
    answer = message.text
    if not validate_email(answer):
        await message.answer(
            'Похоже, вы ввели некорректный адрес электронной почты.\n'
            'Проверьте правильность введённого ранее адреса или попробуйте другой.'
        )
        return
    otp_code = generate_otp()
    await state.update_data(new_email=answer)
    await state.update_data(otp_code=otp_code)
    await state.update_data(prev_state='change_email')
    
    try:
        user = await get_user_by_id(session, message.from_user.id)
    except UserNotFoundException:
        await message.answer('Произошёл непредвиденный сбой, повторите попытку позже')
        await state.clear()
        return
    phone_number = user.phone_number
    await state.update_data(phone_number=phone_number)
    sms_auth.sendSMS(phone_number[1:], f'{otp_code}')
    await state.set_state(Register.confirm_otp)
    await message.answer('Отлично, теперь введите код из СМС, который мы Вам выслали для подтверждения')
