from aiogram import types, Router, Bot
from aiogram.fsm.context import FSMContext

from sqlalchemy.ext.asyncio import AsyncSession

from telegram_bot.states import AdminState

from telegram_bot.utils.validators import validate_phone_number, validate_order_amount

from telegram_bot.db.requests import get_user_by_phone_number, add_bonus_points

from telegram_bot.exceptions import UserNotFoundException

from telegram_bot.keyboards import get_back_to_main_menu_keyboard as back_to_mainmenu_kb

router = Router()


@router.callback_query()
async def add_order(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(AdminState.add_order)
    await callback.message.edit_text(
        'Здесь вы можете добавить новый заказ.\n'
        'Для начала введите номер телефона клиента, который сделал заказ.\n'
        'Пример ввода: +79991234567',
        reply_markup=back_to_mainmenu_kb()
    )
    await state.update_data(prev_state='add_order')
    await state.set_state(AdminState.enter_customer_number)


@router.message()
async def enter_customer_number(message: types.Message, state: FSMContext, session: AsyncSession):
    answer = message.text
    if not validate_phone_number(answer):
        await message.answer(
            'Некорректный формат ввода номера телефона, попробуйте ещё раз.',
            reply_markup=back_to_mainmenu_kb()
        )
        return
    try:
        user = await get_user_by_phone_number(session, answer)
    except UserNotFoundException:
        await message.answer(
            'Не найден пользователь с таким номером телефона, проверьте номер и попробуйте ещё раз.',
            reply_markup=back_to_mainmenu_kb()
            )
        return
    await state.update_data(recipient_phone_number=user.phone_number)
    data = await state.get_data()
    prev_state = data['prev_state']

    if prev_state == 'add_order':
        await message.answer(
            'Теперь введите сумму, на которую клиент совершил заказ.',
            reply_markup=back_to_mainmenu_kb()
        )
        await state.set_state(AdminState.enter_order_amount)
    else:
        await message.answer(
            f'У пользователя с номером телефона {user.phone_number} на счету {user.bonus_points} баллов.\n'
            'Введите новое количество баллов для данного пользователя',
            reply_markup=back_to_mainmenu_kb()
        )
        await state.set_state(AdminState.enter_new_account)


@router.message()
async def enter_order_amount(message: types.Message, state: FSMContext, session: AsyncSession, bot: Bot):
    answer = message.text
    if not validate_order_amount(answer):
        await message.answer(
            'Некорректный формат ввода, попробуйте ещё раз',
            reply_markup=back_to_mainmenu_kb()
        )
        return
    bonus_points_to_add = int(int(answer)*5/100)
    data = await state.get_data()
    phone_number = data['recipient_phone_number']
    try:
        await add_bonus_points(session, bonus_points_to_add, phone_number)
        user = await get_user_by_phone_number(session, phone_number)
    except UserNotFoundException:
        await message.answer(
            'Произошёл сбой, попробуйте заново.',
            reply_markup=back_to_mainmenu_kb()
        )
        return
    await message.answer(
        f'{bonus_points_to_add} баллов успешно зачислено на счёт клиенту с номером: {phone_number}.',
        reply_markup=back_to_mainmenu_kb()
    )
    await state.clear()
    await bot.send_message(
        user.user_id,
        f'Вам зачислено {bonus_points_to_add} баллов! Теперь у вас на счету {user.bonus_points} баллов.'
    )
