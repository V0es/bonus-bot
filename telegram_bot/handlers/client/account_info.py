from aiogram import types

from sqlalchemy.ext.asyncio import AsyncSession

from telegram_bot.keyboards import get_back_to_main_menu_keyboard as back_to_mainmenu_kb
from telegram_bot.db.requests import get_user_by_id
from telegram_bot.exceptions import UserNotFoundException


async def account_info(callback: types.CallbackQuery, session: AsyncSession):
    try:
        user = await get_user_by_id(session, callback.from_user.id)
    except UserNotFoundException:
        await callback.message.edit_text('Непредвиденный сбой. Повторите попытку позже.')
        return
    await callback.message.edit_text(
        f'Баллы, доступные для списания: {user.bonus_points}\n',
        reply_markup=back_to_mainmenu_kb()
    )
