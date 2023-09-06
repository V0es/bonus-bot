from unittest.mock import AsyncMock

import pytest

from telegram_bot.keyboards.back_to_mainmenu import get_back_to_main_menu_keyboard as back_to_mainmenu_kb
from telegram_bot.handlers.client.promotions import promotions


@pytest.mark.asyncio
async def test_promotions():
    call = AsyncMock()

    await promotions(call)
    call.message.edit_text.assert_called_with(
        'Доступные акции для вас:\n\n'
        'Получите 500 бонусных баллов\n'
        'на следующий заказ плюс 5% от\n'
        'стоимости заказа.\n\n'
        
        'При первом заказе вы также\n'
        'получаете начисление 500\n'
        'бонусов и 5% бонусами от\n'
        'стоимости заказа.\n\n'
        
        'Списание баллов:\n\n'
    
        'Бонусная программа позволяет\n'
        'вам оплатить до 30% стоимости\n'
        'заказа баллами.\n\n'
    
        'Бесплатная доставка:\n\n'
    
        'При заказе от 2-ух пар обуви\n'
        'действует бесплатная доставка по\n'
        'Москве.',
        reply_markup=back_to_mainmenu_kb()
    )
