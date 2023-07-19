from .change_email import change_email
from .change_phone import change_phone
from .login import login
from .register import register
from .start import start 

from aiogram import Dispatcher

def register_common_handlers(dp : Dispatcher):
    pass