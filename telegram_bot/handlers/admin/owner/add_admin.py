from aiogram import types
from aiogram.fsm.context import FSMContext


from telegram_bot.states import OwnerState

from telegram_bot.keyboards import get_back_to_main_menu_keyboard as back_to_mainmenu_kb


async def add_admin(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(OwnerState.add_admin)
    await callback.message.edit_text(
        'Введите номер телефона пользователя, которого вы хотите сделать администратором.\n'
        'Формат ввода: +79991234567\n'
        'Учтите, что пользователь уже должен быть зарегистрирован в боте',
        reply_markup=back_to_mainmenu_kb()
    )
    await state.update_data(prev_state='add_admin')
    await state.set_state(OwnerState.enter_admin_phone)
