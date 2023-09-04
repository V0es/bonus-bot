from datetime import datetime

from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.base import StorageKey
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import User, Chat, Message

from tests.test_handlers.mocked_bot import MockedBot

TEST_USER = User(id=1, is_bot=True, first_name='Test', last_name='Bot', username='testbot')

TEST_USER_CHAT = Chat(id=12, type='public', title='testchat',
                      username=TEST_USER.username, first_name=TEST_USER.first_name, last_name=TEST_USER.last_name)


def get_message(text: str, bot: MockedBot) -> Message:
    message = Message(
        message_id=123,
        chat=TEST_USER_CHAT,
        date=datetime.now(),
        from_user=TEST_USER,
        text=text,
        via_bot=TEST_USER
    )
    message._bot = bot
    return message


def create_state(storage: MemoryStorage, bot: MockedBot):
    return FSMContext(
        storage=storage,
        key=StorageKey(bot_id=bot.id, user_id=TEST_USER.id, chat_id=TEST_USER_CHAT.id)
    )
