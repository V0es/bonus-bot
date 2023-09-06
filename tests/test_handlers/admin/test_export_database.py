from datetime import datetime
from unittest.mock import Mock, AsyncMock, PropertyMock, patch
import pytest
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import FSInputFile

from telegram_bot.handlers.admin.export_database import export_database
from telegram_bot.keyboards.back_to_mainmenu import get_back_to_main_menu_keyboard as back_to_mainmenu_kb
from telegram_bot.states import AdminState
from telegram_bot.utils.export import DBExport

from tests.mocked_bot import MockedBot
from tests.utils import create_state


@pytest.mark.asyncio
async def test_export_database(storage: MemoryStorage, bot: MockedBot, mock_datetime: datetime, mocker: Mock):

    call = AsyncMock()
    state = create_state(storage, bot)

    test_dt = datetime(1000,
                       10,
                       10,
                       10,
                       10,
                       10,
                       10)

    mocker.patch(
        'telegram_bot.handlers.admin.export_database.DBExport.upload_to_excel',
        return_value='test')

    # noinspection PyCallingNonCallable
    with mock_datetime('telegram_bot.handlers.admin.export_database.datetime', test_dt):

        await export_database(call, state, AsyncMock())

        call.message.answer_document.assert_called_with(
            document='test',
            caption=f'Выгрузка базы данных пользователей на {test_dt.strftime("%d-%m-%Y_%H-%M-%S")}',
            reply_markup=back_to_mainmenu_kb()
        )
        call.answer.assert_any_call()
        assert await state.get_state() == AdminState.export
