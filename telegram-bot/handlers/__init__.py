from .admin import add_order, export, set_account
from .admin.owner import add_admin, remove_admin

from .client import account_info

from .common import change_email, change_phone, login, register, start

from aiogram import Dispatcher


def _register_admin_handlers(dp: Dispatcher):
    dp.register_message_handler(add_order, commands=['add_order'])
    dp.register_message_handler(export, commands=['export'])
    dp.register_message_handler(set_account, commands=['set_account'])

def _register_owner_handlers(dp: Dispatcher):
    dp.register_message_handler(add_admin, commands=['add_admin'])
    dp.register_message_handler(remove_admin, commands=['remove_admin'])
    

def _register_client_handlers(dp: Dispatcher):
    dp.register_message_handler(account_info, commands=['account_info'])


def _register_common_handlers(dp: Dispatcher):
    dp.register_message_handler(start, commands=['start', 'help'])
    dp.register_message_handler(change_phone, commands=['change_phone'])
    dp.register_message_handler(change_email, commands=['change_email'])
    dp.register_callback_query_handler(login, text='login')
    dp.register_callback_query_handler(register, text='register')
    


def register_handlers(dp: Dispatcher):
    _register_admin_handlers(dp)
    _register_owner_handlers(dp)
    _register_client_handlers(dp)
    _register_common_handlers(dp)