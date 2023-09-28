from aiogram import Router, types
from aiogram.fsm.context import FSMContext

from sqlalchemy.ext.asyncio import AsyncSession

from telegram_bot.keyboards import get_owner_mainmenu_keyboard as owner_mainmenu_kb

from telegram_bot.db.requests import get_user_by_id

from telegram_bot.exceptions import UserNotFoundException

from telegram_bot.states import AdminState, OwnerState

router = Router()


@router.callback_query()
async def owner_main_menu(callback: types.CallbackQuery, state: FSMContext, session: AsyncSession):
    prev_state = await state.get_state()
    await state.clear()
    await state.set_state(OwnerState.main_menu)
    try:
        user = await get_user_by_id(session, callback.from_user.id)
    except UserNotFoundException:
        await callback.message.answer(
            'Упс... Похоже, у нас сбой на сервере, мы уже работаем над исправлением, зайдите чуть попозже'
        )
        return
    if prev_state == AdminState.export:
        await callback.message.edit_reply_markup(reply_markup=None)
        await callback.message.answer(
            f'Доброго времени стуток, {user.fullname}!\n'
            'Вы находитесь в панели владельца.\n'
            'Здесь вы можете создать новый заказ, изменить баллы пользователей, '
            'выгрузить данные и редактировать список администраторов.',
            reply_markup=owner_mainmenu_kb()
        )

    else:
        await callback.message.edit_text(
            f'Доброго времени стуток, {user.fullname}!\n'
            'Вы находитесь в панели владельца.\n'
            'Здесь вы можете создать новый заказ, изменить баллы пользователей, '
            'выгрузить данные и редактировать список администраторов.',
            reply_markup=owner_mainmenu_kb()
        )
