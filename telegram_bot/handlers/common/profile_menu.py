from aiogram import Router, types
from aiogram.fsm.context import FSMContext

from sqlalchemy.ext.asyncio import AsyncSession

from states import UserState

from db.requests import get_user_by_id

from keyboards import get_profile_keyboard as get_profile_kb


async def profile_menu(callback: types.CallbackQuery, state: FSMContext, session: AsyncSession):
    await state.set_state(UserState.profile_menu)
    user = await get_user_by_id(session, callback.from_user.id)

    if not (user.is_admin and user.is_owner):
        role = 'Клиент'
    elif user.is_admin and not user.is_owner:
        role = 'Администратор'
    else:
        role = 'Владелец'

    await callback.message.edit_text(
        f'Номер телефона: {user.phone_number}\n'
        f'Имя: {user.fullname}\n'
        f'Email: {user.email}\n'
        f'Роль: {role}',
        reply_markup=get_profile_kb()
    )
