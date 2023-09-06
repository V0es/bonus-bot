from unittest.mock import AsyncMock, Mock

import pytest
from aiogram.fsm.storage.memory import MemoryStorage

from telegram_bot.handlers import change_email, enter_new_email
from telegram_bot.states import UserState, Register
from tests.mocked_bot import MockedBot
from tests.utils import create_state


@pytest.mark.asyncio
async def test_change_email(storage: MemoryStorage, bot: MockedBot):
    call = AsyncMock()
    state = create_state(storage, bot)
    await change_email(call, state)

    assert await state.get_state() == UserState.change_email
    call.message.edit_text.assert_called_with('Введите новый email')


@pytest.mark.asyncio
async def test_enter_new_email(storage: MemoryStorage, bot: MockedBot, mocker: Mock):
    message = AsyncMock()
    state = create_state(storage, bot)
    mocker.patch('telegram_bot.handlers.common.change_email.get_user_by_id')

    # Valid email
    message.text = 'test@test.test'
    await enter_new_email(message, state, AsyncMock())
    assert await state.get_state() == Register.confirm_otp
    message.answer.assert_called_with(
        'Отлично, теперь введите код, который Вам продиктует бот из входящего звонка.'
    )

    # Invalid email
    await state.set_state(UserState.change_email)  # set initial state
    message.text = '@test.@test'
    await enter_new_email(message, state, AsyncMock())
    assert await state.get_state() == UserState.change_email
    message.answer.assert_called_with(
        'Похоже, вы ввели некорректный адрес электронной почты.\n'
        'Проверьте правильность введённого ранее адреса или попробуйте другой.'
    )
    