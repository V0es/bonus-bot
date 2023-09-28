from unittest.mock import AsyncMock

import pytest

from telegram_bot.keyboards.back_to_mainmenu import get_back_to_main_menu_keyboard as back_to_mainmenu_kb
from telegram_bot.handlers.client.support import support


@pytest.mark.asyncio
async def test_support():
    call = AsyncMock()

    await support(call)
    call.message.edit_text.assert_called_with(
        'Контакты службы поддержки:\n'
        '@byandcleanmanager',
        reply_markup=back_to_mainmenu_kb()
    )
