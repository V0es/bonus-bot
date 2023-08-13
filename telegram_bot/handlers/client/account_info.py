from aiogram import types

from sqlalchemy.ext.asyncio import AsyncSession

from keyboards import get_back_to_main_menu_keyboard as back_kb
from db.requests import get_user_by_id
from exceptions import UserNotFoundException


async def account_info(callback: types.CallbackQuery, session: AsyncSession):
    try:
        user = await get_user_by_id(session, callback.from_user.id)
    except UserNotFoundException:
        await callback.message.edit_text('Непредвиденный сбой. Повторите попытку позже.')
        return
    await callback.message.edit_text(
        f'Баллы, доступные для списания: {user.bonus_points}\n'
        f'Последнее пополнение: {user.last_scoring.strftime("%H:%M:%S %d.%m.%Y") if user.last_scoring else "пополнений пока не было"}\n',
        reply_markup=back_kb()
    )
