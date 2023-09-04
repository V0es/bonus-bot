import pytest
import pytest_asyncio
from aiogram import Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.methods import Response

from tests.test_handlers.mocked_bot import MockedBot


@pytest_asyncio.fixture()
async def storage():
    tmp_storage = MemoryStorage()
    try:
        yield tmp_storage
    finally:
        await tmp_storage.close()


@pytest.fixture()
def bot():
    bot = MockedBot()
    bot.session.add_result(Response(ok=True))
    return bot


@pytest_asyncio.fixture()
async def dispatcher():
    dp = Dispatcher()
    await dp.emit_startup()
    try:
        yield dp
    finally:
        await dp.emit_shutdown()