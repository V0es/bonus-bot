from unittest.mock import AsyncMock, Mock

import pytest
from aiogram.fsm.storage.memory import MemoryStorage

from telegram_bot.db.models import User
from telegram_bot.keyboards.admin_keyboard import get_admin_mainmenu_keyboard as admin_mainmenu_kb
from telegram_bot.states import AdminState

from tests.mocked_bot import MockedBot
from tests.utils import create_state

from telegram_bot.handlers.admin.main_menu import admin_main_menu


@pytest.mark.asyncio
async def test_admin_main_menu(storage: MemoryStorage, bot: MockedBot, mocker: Mock):
    call = AsyncMock()
    state = create_state(storage, bot)

    # noinspection PyArgumentList
    mocker.patch(
        'telegram_bot.handlers.admin.main_menu.get_user_by_id',
        return_value=User(
            fullname='Test',
        )
    )

    await admin_main_menu(call, state, AsyncMock())

    # Without prev state
    call.message.edit_text.assert_called_with(
        f'Доброго времени стуток, Test!\n'
        'Вы находитесь в админской панели.\n'
        'Здесь вы можете создать новый заказ, изменить баллы пользователей, '
        'выгрузить данные и редактировать свой профиль.',
        reply_markup=admin_mainmenu_kb()
    )
    assert await state.get_state() == AdminState.main_menu

    # With prev state
    await state.set_state(AdminState.export)
    await admin_main_menu(call, state, AsyncMock())

    call.message.answer.assert_called_with(
        f'Доброго времени стуток, Test!\n'
        'Вы находитесь в админской панели.\n'
        'Здесь вы можете создать новый заказ, изменить баллы пользователей, '
        'выгрузить данные и редактировать свой профиль.',
        reply_markup=admin_mainmenu_kb()
    )
    assert await state.get_state() == AdminState.main_menu
