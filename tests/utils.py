from aiogram.types import User, Chat

TEST_USER = User(id=1, is_bot=False, first_name='Test', last_name='Bot', username='testbot')

TEST_USER_CHAT = Chat(id=12, type='public', title='testchat',
                      username=TEST_USER.username, first_name=TEST_USER.first_name, last_name=TEST_USER.last_name)
