from unittest.mock import AsyncMock, Mock

import pytest
from aiogram.fsm.storage.memory import MemoryStorage

from telegram_bot.handlers import remove_admin
from telegram_bot.states import OwnerState
from telegram_bot.keyboards.back_to_mainmenu import get_back_to_main_menu_keyboard as back_to_mainmenu_kb

from tests.mocked_bot import MockedBot
from tests.utils import create_state


@pytest.mark.asyncio
async def test_remove_admin(storage: MemoryStorage, bot: MockedBot, mocker: Mock):
    call = AsyncMock()
    state = create_state(storage, bot)

    await remove_admin(call, state)

    call.message.edit_text.assert_called_with(
        'Введите номер телефона пользователя, которого вы хотите исключить из администраторов.\n'
        'Формат ввода: +79991234567\n',
        reply_markup=back_to_mainmenu_kb()
    )
    assert await state.get_state() == OwnerState.enter_admin_phone
