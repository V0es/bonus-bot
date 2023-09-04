from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from aiogram.fsm.storage.memory import MemoryStorage
from sqlalchemy.ext.asyncio import AsyncSession

import telegram_bot
from telegram_bot.db.models import User
from telegram_bot.handlers.common.profile_menu import profile_menu
from telegram_bot.states import UserState
from tests.test_handlers.mocked_bot import MockedBot
from tests.utils import create_state

from telegram_bot.keyboards.profile_keyboard import get_profile_keyboard as get_profile_kb


@pytest.mark.asyncio
async def test_profile_menu(storage: MemoryStorage, bot: MockedBot, mocker):
    pass
