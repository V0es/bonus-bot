from aiogram import types, Bot
from aiogram.fsm.context import FSMContext
from sqlalchemy.ext.asyncio import AsyncSession

from keyboards import get_back_to_main_menu_keyboard as back_to_mainmenu_kb
from utils.validators import validate_phone_number
from exceptions import UserNotFoundException
from db.requests import get_user_by_phone_number, is_admin, set_admin, remove_admin
from states import OwnerState


async def enter_admin_phone(message: types.Message, state: FSMContext, session: AsyncSession, bot: Bot):
    phone_number = message.text
    prev_state = await state.get_state()
    if not validate_phone_number(phone_number):
        await message.answer(
            'Неверный формат ввода, попробуйте ввести ещё раз или вернитесь в главное меню',
            reply_markup=back_to_mainmenu_kb()
        )
        return
    try:
        user = await get_user_by_phone_number(session, phone_number)
    except UserNotFoundException:
        await message.answer(
            'Пользователь с таким номером телефона не найден.\n'
            'Чтобы добавить или убрать пользователя из администраторов, он должен быть зарегистрирован в боте.',
            reply_markup=back_to_mainmenu_kb()
        )
        return

    admin_flag = await is_admin(session, user.user_id)
    data = await state.get_data()
    prev_state = data['prev_state']

    if prev_state == 'add_admin':
        if admin_flag:
            await message.answer(
                'Этот пользователь уже является администратором!',
                reply_markup=back_to_mainmenu_kb()
            )
            return
        await set_admin(session, phone_number)
        await message.answer(
            f'Пользователь с номером {phone_number} успешно назначен администратором!',
            reply_markup=back_to_mainmenu_kb()
        )
        await bot.send_message(
            user.user_id,
            'Вы были назначены администратором бота!\n'
            'Чтобы перейти в админскую панель, перезайдите в главное меню.',
            reply_markup=back_to_mainmenu_kb()
        )

    elif prev_state == 'remove_admin':
        if not admin_flag:
            await message.answer(
                'Этот пользователь и так не является администратором!',
                reply_markup=back_to_mainmenu_kb()
            )
            return
        await remove_admin(session, phone_number)
        await message.answer(
            f'Пользователь с номером {phone_number} успешно исключён из администраторов!',
            reply_markup=back_to_mainmenu_kb()
        )
        await bot.send_message(
            user.user_id,
            'Вы были исключены из администраторов бота!\n'
            'Админская панель вам больше недоступна',
            reply_markup=back_to_mainmenu_kb()
        )
