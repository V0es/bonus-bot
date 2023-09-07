from unittest.mock import AsyncMock, Mock

import pytest
from aiogram.fsm.storage.memory import MemoryStorage

from telegram_bot.db.models import User
from telegram_bot.states import AdminState
from tests.mocked_bot import MockedBot
from tests.utils import create_state

from telegram_bot.handlers.admin.add_order import add_order, enter_customer_number, enter_order_amount
from telegram_bot.keyboards.back_to_mainmenu import get_back_to_main_menu_keyboard as back_to_mainmenu_kb


@pytest.mark.asyncio
async def test_add_order(storage: MemoryStorage, bot: MockedBot):
    call = AsyncMock()
    state = create_state(storage, bot)

    await add_order(call, state)

    call.message.edit_text.assert_called_with(
        'Здесь вы можете добавить новый заказ.\n'
        'Для начала введите номер телефона клиента, который сделал заказ.\n'
        'Пример ввода: +79991234567',
        reply_markup=back_to_mainmenu_kb()
    )
    assert await state.get_state() == AdminState.enter_customer_number


@pytest.mark.asyncio
async def test_enter_customer_number(storage: MemoryStorage, bot: MockedBot, mocker: Mock):
    message = AsyncMock()
    state = create_state(storage, bot)

    # noinspection PyArgumentList
    mocker.patch(
        'telegram_bot.handlers.admin.add_order.get_user_by_phone_number',
        return_value=User(
            phone_number='test',
            bonus_points=123
        )
    )

    # Valid number
    await state.update_data(prev_state='test')
    message.text = '+70000000000'
    await enter_customer_number(message, state, AsyncMock())
    message.answer.assert_called_with(
        f'У пользователя с номером телефона test на счету 123 баллов.\n'
        'Введите новое количество баллов для данного пользователя',
        reply_markup=back_to_mainmenu_kb()
    )
    assert await state.get_state() == AdminState.enter_new_account

    # Invalid number
    message.text = '+@234'
    await state.update_data(prev_state='test')
    await enter_customer_number(message, state, AsyncMock())

    message.answer.assert_called_with(
        'Некорректный формат ввода номера телефона, попробуйте ещё раз.',
        reply_markup=back_to_mainmenu_kb()
    )

    # Valid with prev state
    message.text = '+70000000000'
    await state.update_data(prev_state='add_order')
    await enter_customer_number(message, state, AsyncMock())

    message.answer.assert_called_with(
        'Теперь введите сумму, на которую клиент совершил заказ.',
        reply_markup=back_to_mainmenu_kb()
    )
    assert await state.get_state() == AdminState.enter_order_amount


@pytest.mark.asyncio
async def test_enter_order_amount(storage: MemoryStorage, bot: MockedBot, mocker: Mock):
    mocker.patch(
        'telegram_bot.handlers.admin.add_order.add_bonus_points'
    )
    message = AsyncMock()
    state = create_state(storage, bot)
    await state.update_data(recipient_phone_number='test')
    # noinspection PyArgumentList
    mocker.patch(
        'telegram_bot.handlers.admin.add_order.get_user_by_phone_number',
        return_value=User(
            user_id=123,
            bonus_points=123
        )
    )
    # Valid amount
    message.text = '123'
    await enter_order_amount(message, state, AsyncMock(), bot)

    message.answer.assert_called_with(
        f'{int(123*0.05)} баллов успешно зачислено на счёт клиенту с номером: test.',
        reply_markup=back_to_mainmenu_kb()
    )

    # Invalid amount
    message.text = 'ff4@'
