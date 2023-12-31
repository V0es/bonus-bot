from aiogram import types, Router
from aiogram.fsm.context import FSMContext

from sqlalchemy.ext.asyncio import AsyncSession

from telegram_bot.keyboards import get_client_mainmenu_keyboard as client_mainmenu_kb

from telegram_bot.exceptions import UserNotFoundException

from telegram_bot.db.requests import get_user_by_id

from telegram_bot.states import UserState


router = Router()


@router.callback_query()
async def client_main_menu(callback: types.CallbackQuery, state: FSMContext, session: AsyncSession) -> None:
    await state.clear()
    await state.set_state(UserState.main_menu)
    try:
        user = await get_user_by_id(session, callback.from_user.id)
    except UserNotFoundException:
        await callback.message.answer(
            'Упс... Похоже, у нас сбой на сервере, мы уже работаем над исправлением, зайдите чуть попозже'
        )
        return
    await callback.message.edit_text(
        f'Доброго времени суток, {user.fullname}.\n'
        'Вы находитесь в главном меню бота.\n'
        'Здесь вы можете посмотреть баланс баллов, перейти в свой профиль и увидеть новые промоакции.',
        reply_markup=client_mainmenu_kb())

    await callback.answer()
