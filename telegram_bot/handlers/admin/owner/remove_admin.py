from aiogram import types
from aiogram.fsm.context import FSMContext

from telegram_bot.states import OwnerState
from telegram_bot.keyboards import get_back_to_main_menu_keyboard as back_to_mainmenu_kb


async def remove_admin(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(OwnerState.add_admin)
    await callback.message.edit_text(
        'Введите номер телефона пользователя, которого вы хотите исключить из администраторов.\n'
        'Формат ввода: +79991234567\n',
        reply_markup=back_to_mainmenu_kb()
    )
    await state.update_data(prev_state='remove_admin')
    await state.set_state(OwnerState.enter_admin_phone)
