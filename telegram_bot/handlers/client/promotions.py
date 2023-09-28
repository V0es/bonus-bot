from aiogram import types

from telegram_bot.keyboards import get_back_to_main_menu_keyboard as back_to_mainmenu_kb


async def promotions(callback: types.CallbackQuery):
    await callback.message.edit_text(
        '''Доступные акции для вас:

Получите 500 бонусных баллов
на следующий заказ плюс 5% от
стоимости заказа.

При первом заказе вы также
получаете начисление 500
бонусов и 5% бонусами от
стоимости заказа.

Списание баллов:

Бонусная программа позволяет
вам оплатить до 30% стоимости
заказа баллами.

Бесплатная доставка:

При заказе от 2-ух пар обуви
действует бесплатная доставка по
Москве.''',
        reply_markup=back_to_mainmenu_kb()
    )
