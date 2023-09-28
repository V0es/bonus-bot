from unittest.mock import AsyncMock, Mock

import pytest
from aiogram.fsm.storage.memory import MemoryStorage

from telegram_bot.db.models import User
from telegram_bot.handlers import enter_admin_phone
from telegram_bot.keyboards.back_to_mainmenu import get_back_to_main_menu_keyboard as back_to_mainmenu_kb

from tests.mocked_bot import MockedBot
from tests.utils import create_state


@pytest.mark.asyncio
async def test_enter_admin_phone(storage: MemoryStorage, bot: MockedBot, mocker: Mock):
    message = AsyncMock()
    state = create_state(storage, bot)

    # noinspection PyArgumentList
    mocker.patch(
        'telegram_bot.handlers.admin.owner.enter_admin_phone.get_user_by_phone_number',
        return_value=User(
            user_id=123
        )
    )

    message.text = '+70000000000'

    # Prev state add admin, already admin
    mocker.patch(
        'telegram_bot.handlers.admin.owner.enter_admin_phone.is_admin',
        return_value=True
    )

    await state.update_data(prev_state='add_admin')
    await enter_admin_phone(message, state, AsyncMock(), bot)

    message.answer.assert_called_with(
        'Этот пользователь уже является администратором!',
        reply_markup=back_to_mainmenu_kb()
    )

    # Prev state add admin, not admin
    mocker.patch(
        'telegram_bot.handlers.admin.owner.enter_admin_phone.is_admin',
        return_value=False
    )
    await enter_admin_phone(message, state, AsyncMock(), bot)

    message.answer.assert_called_with(
        f'Пользователь с номером {message.text} успешно назначен администратором!',
        reply_markup=back_to_mainmenu_kb()
    )

    # Prev state remove admin, not admin
    await state.update_data(prev_state='remove_admin')
    await enter_admin_phone(message, state, AsyncMock(), bot)

    message.answer.assert_called_with(
        'Этот пользователь и так не является администратором!',
        reply_markup=back_to_mainmenu_kb()
    )

    # Prev state remove admin, already admin
    mocker.patch(
        'telegram_bot.handlers.admin.owner.enter_admin_phone.is_admin',
        return_value=True
    )
    await enter_admin_phone(message, state, AsyncMock(), bot)

    message.answer.assert_called_with(
        f'Пользователь с номером {message.text} успешно исключён из администраторов!',
        reply_markup=back_to_mainmenu_kb()
    )

    # Invalid phone number
    message.text = '+72sdf@'
    await enter_admin_phone(message, state, AsyncMock(), bot)

    message.answer.assert_called_with(
        'Неверный формат ввода, попробуйте ввести ещё раз или вернитесь в главное меню',
        reply_markup=back_to_mainmenu_kb()
    )


