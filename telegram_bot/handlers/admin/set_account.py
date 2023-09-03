from aiogram import types
from aiogram.fsm.context import FSMContext
from sqlalchemy.ext.asyncio import AsyncSession

from telegram_bot.keyboards import get_back_to_main_menu_keyboard as back_to_mainmenu_kb
from telegram_bot.utils.validators import validate_order_amount
from telegram_bot.db.requests import change_bonus_points
from telegram_bot.exceptions import UserNotFoundException

from telegram_bot.states import AdminState


async def set_account(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(AdminState.set_account)
    await callback.message.edit_text(
        'Введите номер телефона пользователя, баланс которого вы хотите изменить.\n'
        'Пример ввода: +79991234567',
        reply_markup=back_to_mainmenu_kb()
    )
    await state.update_data(prev_state='set_account')
    await state.set_state(AdminState.enter_customer_number)


async def enter_new_account(message: types.Message, state: FSMContext, session: AsyncSession):
    new_account = message.text
    if not validate_order_amount(new_account):
        await message.answer(
            'Неправильный формат ввода, попробуйте ввести ещё раз или вернитесь в главное меню',
            reply_markup=back_to_mainmenu_kb()
        )
        return
    data = await state.get_data()
    recipients_phone_number = data['recipient_phone_number']
    try:
        await change_bonus_points(session, recipients_phone_number, int(new_account))
    except UserNotFoundException:
        await message.answer(
            'Произошёл сбой, попробуйте заново.',
            reply_markup=back_to_mainmenu_kb()
        )
        return
    await message.answer(
        'Баллы успешно изменены.',
        reply_markup=back_to_mainmenu_kb()
    )
