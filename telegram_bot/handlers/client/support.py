from aiogram import types

from telegram_bot.keyboards import get_back_to_main_menu_keyboard as back_to_mainmenu_kb


async def support(callback: types.CallbackQuery):
    await callback.message.edit_text(
        'Контакты службы поддержки:\n'
        '@byandcleanmanager',
        reply_markup=back_to_mainmenu_kb()
    )
    await callback.answer()
