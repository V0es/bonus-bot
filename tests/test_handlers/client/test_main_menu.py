from unittest.mock import AsyncMock, Mock

import pytest
from aiogram.fsm.storage.memory import MemoryStorage

from telegram_bot.db.models import User
from telegram_bot.keyboards.client_keyboard import get_client_mainmenu_keyboard as client_mainmenu_kb
from telegram_bot.states import UserState

from tests.mocked_bot import MockedBot
from tests.utils import create_state

from telegram_bot.handlers.client.main_menu import client_main_menu


@pytest.mark.asyncio
async def test_client_main_menu(storage: MemoryStorage, bot: MockedBot, mocker: Mock):
    call = AsyncMock()
    state = create_state(storage, bot)

    # noinspection PyArgumentList
    mocker.patch(
        'telegram_bot.handlers.client.main_menu.get_user_by_id',
        return_value=User(
            fullname='Test',
        )
    )

    await client_main_menu(call, state, AsyncMock())

    call.message.edit_text.assert_called_with(
        f'Доброго времени суток, Test.\n'
        'Вы находитесь в главном меню бота.\n'
        'Здесь вы можете посмотреть баланс баллов, перейти в свой профиль и увидеть новые промоакции.',
        reply_markup=client_mainmenu_kb()
    )
    assert await state.get_state() == UserState.main_menu

