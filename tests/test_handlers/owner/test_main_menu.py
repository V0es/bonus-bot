from unittest.mock import AsyncMock, Mock

import pytest
from aiogram.fsm.storage.memory import MemoryStorage

from telegram_bot.db.models import User
from telegram_bot.handlers import owner_main_menu
from telegram_bot.states import AdminState, OwnerState
from telegram_bot.keyboards.owner_keyboard import get_owner_mainmenu_keyboard as owner_mainmenu_kb

from tests.mocked_bot import MockedBot
from tests.utils import create_state


@pytest.mark.asyncio
async def test_main_menu(storage: MemoryStorage, bot: MockedBot, mocker: Mock):
    call = AsyncMock()
    state = create_state(storage, bot)
    test_fullname = 'Test'

    # noinspection PyArgumentList
    mocker.patch(
        'telegram_bot.handlers.admin.owner.main_menu.get_user_by_id',
        return_value=User(
            fullname=test_fullname
        )
    )

    # No prev state
    await owner_main_menu(call, state, AsyncMock())
    call.message.edit_text.assert_called_with(
        f'Доброго времени стуток, {test_fullname}!\n'
        'Вы находитесь в панели владельца.\n'
        'Здесь вы можете создать новый заказ, изменить баллы пользователей, '
        'выгрузить данные и редактировать список администраторов.',
        reply_markup=owner_mainmenu_kb()
    )
    assert await state.get_state() == OwnerState.main_menu

    # Export prev state
    await state.clear()
    await state.set_state(AdminState.export)
    await owner_main_menu(call, state, AsyncMock())

    call.message.answer.assert_called_with(
        f'Доброго времени стуток, {test_fullname}!\n'
        'Вы находитесь в панели владельца.\n'
        'Здесь вы можете создать новый заказ, изменить баллы пользователей, '
        'выгрузить данные и редактировать список администраторов.',
        reply_markup=owner_mainmenu_kb()
    )
    assert await state.get_state() == OwnerState.main_menu
