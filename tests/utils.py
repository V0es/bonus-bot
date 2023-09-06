from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.base import StorageKey
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import User, Chat

from tests.mocked_bot import MockedBot

TEST_USER = User(id=1, is_bot=True, first_name='Test', last_name='Bot', username='testbot')

TEST_USER_CHAT = Chat(id=12, type='public', title='testchat',
                      username=TEST_USER.username, first_name=TEST_USER.first_name, last_name=TEST_USER.last_name)


def create_state(storage: MemoryStorage, bot: MockedBot):
    return FSMContext(
        storage=storage,
        key=StorageKey(bot_id=bot.id, user_id=TEST_USER.id, chat_id=TEST_USER_CHAT.id)
    )
