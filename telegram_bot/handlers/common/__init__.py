from aiogram import Router, F
from aiogram.filters import CommandStart

from sqlalchemy.orm import sessionmaker

from .change_email import change_email
from .change_phone import change_phone
from .login import login
from .register import register, enter_fullname, enter_email, enter_phone_number, resend_otp, confirm_otp
from .start import start_registered, start_unregistered
from .profile_menu import profile_menu

from states import Register, UserState
from filters import IsRegistered


def register_common_handlers(router: Router, session_pool: sessionmaker) -> None:
    router.message.register(start_unregistered, CommandStart(), ~IsRegistered(session_pool))
    router.message.register(start_registered, CommandStart(), IsRegistered(session_pool))
    router.message.register(enter_fullname, Register.enter_fullname)
    router.message.register(enter_phone_number, Register.enter_phone_number)
    router.message.register(enter_email, Register.enter_email)
    router.message.register(confirm_otp, Register.confirm_otp)

    router.callback_query.register(profile_menu, IsRegistered(session_pool), F.data == 'profile_menu', UserState.main_menu)
    router.callback_query.register(register, F.data == 'register')
    router.callback_query.register(resend_otp, Register.resend_otp)
