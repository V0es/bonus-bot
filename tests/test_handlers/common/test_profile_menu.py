from unittest.mock import AsyncMock, Mock

import pytest
from aiogram.fsm.storage.memory import MemoryStorage

from telegram_bot.db.models import User
from telegram_bot.handlers.common.profile_menu import profile_menu
from telegram_bot.states import UserState
from tests.mocked_bot import MockedBot
from tests.utils import create_state


from telegram_bot.keyboards.profile_keyboard import get_profile_keyboard as get_profile_kb


@pytest.mark.asyncio
async def test_profile_menu(storage: MemoryStorage, bot: MockedBot, mocker: Mock):
    # noinspection PyArgumentList
    mocker.patch(
        'telegram_bot.handlers.common.profile_menu.get_user_by_id',
        return_value=User(
            fullname='Test Test',
            phone_number='test',
            email='test',
            is_admin=True,
            is_owner=True
        ))
    call = AsyncMock()
    state = create_state(storage, bot)
    await profile_menu(call, state, AsyncMock())
    call.message.edit_text.assert_called_with(
        f'Номер телефона: test\n'
        f'Имя: Test Test\n'
        f'Email: test\n'
        f'Роль: Владелец',
        reply_markup=get_profile_kb()
    )
    assert await state.get_state() == UserState.profile_menu
