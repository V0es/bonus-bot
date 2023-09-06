from unittest.mock import AsyncMock, Mock

import pytest
from aiogram.fsm.storage.memory import MemoryStorage

from telegram_bot.handlers.common.change_phone import change_phone, enter_new_phone
from telegram_bot.states import UserState, Register
from tests.mocked_bot import MockedBot
from tests.utils import create_state


@pytest.mark.asyncio
async def test_change_phone(storage: MemoryStorage, bot: MockedBot):
    call = AsyncMock()
    state = create_state(storage, bot)
    await change_phone(call, state)

    assert await state.get_state() == UserState.change_phone_number
    call.message.edit_text.assert_called_with('Введите новый номер телефона, например +79991234567')


@pytest.mark.asyncio
async def test_enter_new_phone(storage: MemoryStorage, bot: MockedBot, mocker: Mock):
    mocker.patch('telegram_bot.handlers.common.change_phone.get_user_by_id')
    message = AsyncMock()
    message.text = '+70000000000'
    state = create_state(storage, bot)
    await enter_new_phone(message, state, AsyncMock())

    assert await state.get_state() == Register.confirm_otp
    message.answer.assert_called_with(
        'Отлично, теперь введите код из СМС, который мы Вам выслали на старый номер для подтверждения'
    )
