import pytest
import pytest_asyncio
from aiogram import Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.methods import Response

from tests.mocked_bot import MockedBot
from tests.mocked_datetime import MockDatetime


@pytest_asyncio.fixture()
async def storage():
    tmp_storage = MemoryStorage()
    try:
        yield tmp_storage
    finally:
        await tmp_storage.close()


@pytest_asyncio.fixture()
async def bot():
    bot = MockedBot()
    bot.session.add_result(Response(ok=True))
    yield bot


@pytest_asyncio.fixture()
async def dispatcher():
    dp = Dispatcher()
    await dp.emit_startup()
    try:
        yield dp
    finally:
        await dp.emit_shutdown()


@pytest_asyncio.fixture()
async def mock_datetime():
    dt_mock = MockDatetime
    yield dt_mock
