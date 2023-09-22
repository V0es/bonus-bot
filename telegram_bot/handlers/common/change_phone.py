from aiogram import types, Router
from aiogram.fsm.context import FSMContext

from sqlalchemy.ext.asyncio import AsyncSession

from telegram_bot.states import UserState, Register

from telegram_bot.exceptions import UserNotFoundException

from telegram_bot.utils.validators import validate_phone_number
from telegram_bot.utils.otp import generate_otp
from telegram_bot.utils.web import sms_auth

from telegram_bot.keyboards.confirm_otp_keyboard import confirm_otp_keyboard as confirm_otp_kb

from telegram_bot.db.requests import get_user_by_id


router = Router()


@router.callback_query()
async def change_phone(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(UserState.change_phone_number)
    await callback.message.edit_text('Введите новый номер телефона, например +79991234567')


@router.message()
async def enter_new_phone(message: types.Message, state: FSMContext, session: AsyncSession):
    new_phone_number = message.text

    if not validate_phone_number(new_phone_number):
        await message.answer('Неверный формат номера телефона, попробуйте ещё раз.')
        return

    otp_code = generate_otp()
    await state.update_data(new_phone_number=new_phone_number)
    await state.update_data(otp_code=otp_code)
    await state.update_data(prev_state='change_phone_number')

    try:
        user = await get_user_by_id(session, message.from_user.id)
    except UserNotFoundException:
        await message.answer('Произошёл непредвиденный сбой, повторите попытку позже')
        await state.clear()
        return
    old_phone_number = user.phone_number
    await state.update_data(phone_number=old_phone_number)
    sms_auth.sendSMS(old_phone_number[1:], f'{otp_code}')
    await state.set_state(Register.confirm_otp)
    await message.answer(
        'Отлично, теперь введите код из СМС, который мы Вам выслали на старый номер для подтверждения',
        reply_markup=confirm_otp_kb)
