from unittest.mock import AsyncMock

import pytest
from aiogram.fsm.storage.memory import MemoryStorage

from telegram_bot.states import OwnerState
from tests.mocked_bot import MockedBot

from telegram_bot.handlers.admin.owner.add_admin import add_admin
from telegram_bot.keyboards.back_to_mainmenu import get_back_to_main_menu_keyboard as back_to_mainmenu_kb
from tests.utils import create_state


@pytest.mark.asyncio
async def test_add_admin(storage: MemoryStorage, bot: MockedBot):
    call = AsyncMock()
    state = create_state(storage, bot)

    await add_admin(call, state)

    call.message.edit_text.assert_called_with(
        'Введите номер телефона пользователя, которого вы хотите сделать администратором.\n'
        'Формат ввода: +79991234567\n'
        'Учтите, что пользователь уже должен быть зарегистрирован в боте',
        reply_markup=back_to_mainmenu_kb()
    )

    assert await state.get_state() == OwnerState.enter_admin_phone