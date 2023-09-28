from unittest.mock import AsyncMock, Mock

import pytest
from aiogram.fsm.storage.memory import MemoryStorage

from telegram_bot.handlers.common.change_fullname import change_fullname, enter_new_fullname
from telegram_bot.states import UserState
from tests.mocked_bot import MockedBot
from tests.utils import create_state

from telegram_bot.keyboards.back_to_mainmenu import get_back_to_main_menu_keyboard as back_to_mainmenu_kb


@pytest.mark.asyncio
async def test_change_fullname(storage: MemoryStorage, bot: MockedBot):
    call = AsyncMock()
    state = create_state(storage, bot)
    await change_fullname(call, state)

    assert await state.get_state() == UserState.change_fullname
    call.message.edit_text.assert_called_with('Введите новое имя')


@pytest.mark.asyncio
async def test_enter_new_fullname(storage: MemoryStorage, bot: MockedBot, mocker: Mock):
    mocker.patch('telegram_bot.handlers.common.change_fullname.change_user_fullname')
    message = AsyncMock()
    state = create_state(storage, bot)

    # Valid name
    message.text = 'Test'
    await state.set_state(UserState.change_fullname)  # set initial state
    await enter_new_fullname(message, state, AsyncMock())

    assert await state.get_state() is None
    message.answer.assert_called_with(
        'Имя успешно изменено!', reply_markup=back_to_mainmenu_kb()
    )

    # Invalid name
    message.text = 'Test@'
    await state.set_state(UserState.change_fullname)  # set initial state
    await enter_new_fullname(message, state, AsyncMock())

    assert await state.get_state() == UserState.change_fullname  # check if state didn't change
    message.answer.assert_called_with(
        'Вы ввели некорректное имя, попробуйте ещё раз', reply_markup=back_to_mainmenu_kb()
    )
