from unittest.mock import AsyncMock, Mock

import pytest

from telegram_bot.db.models import User
from telegram_bot.handlers.client.account_info import account_info
from telegram_bot.keyboards.back_to_mainmenu import get_back_to_main_menu_keyboard as back_to_mainmenu_kb


@pytest.mark.asyncio
async def test_account_info(mocker: Mock):
    call = AsyncMock()

    # noinspection PyArgumentList
    mocker.patch(
        'telegram_bot.handlers.client.account_info.get_user_by_id',
        return_value=User(
            bonus_points=123
        )
    )

    await account_info(call, AsyncMock())

    call.message.edit_text.assert_called_with(
        f'Баллы, доступные для списания: 123\n',
        reply_markup=back_to_mainmenu_kb()
    )

