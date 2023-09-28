from unittest.mock import AsyncMock, Mock

import pytest
from aiogram.fsm.storage.memory import MemoryStorage

from telegram_bot.handlers.admin.set_account import set_account, enter_new_account
from telegram_bot.keyboards.back_to_mainmenu import get_back_to_main_menu_keyboard as back_to_mainmenu_kb
from telegram_bot.states import AdminState

from tests.mocked_bot import MockedBot
from tests.utils import create_state


@pytest.mark.asyncio
async def test_set_account(storage: MemoryStorage, bot: MockedBot):
    call = AsyncMock()
    state = create_state(storage, bot)

    await set_account(call, state)

    call.message.edit_text.assert_called_with(
        'Введите номер телефона пользователя, баланс которого вы хотите изменить.\n'
        'Пример ввода: +79991234567',
        reply_markup=back_to_mainmenu_kb()
    )
    assert await state.get_state() == AdminState.enter_customer_number


@pytest.mark.asyncio
async def test_enter_new_account(storage: MemoryStorage, bot: MockedBot, mocker: Mock):
    message = AsyncMock()
    state = create_state(storage, bot)
    await state.update_data(recipient_phone_number='123')

    mocker.patch(
        'telegram_bot.handlers.admin.set_account.change_bonus_points'
    )

    # Valid data
    message.text = '123'
    await enter_new_account(message, state, AsyncMock())
    message.answer.assert_called_with(
        'Баллы успешно изменены.',
        reply_markup=back_to_mainmenu_kb()
    )
    assert await state.get_state() is None

    # Invalid data
    message.text = '1df@'
    await enter_new_account(message, state, AsyncMock())
    message.answer.assert_called_with(
        'Неправильный формат ввода, попробуйте ввести ещё раз или вернитесь в главное меню',
        reply_markup=back_to_mainmenu_kb()
    )
