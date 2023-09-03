from aiogram import Router, F
from aiogram.filters import CommandStart, or_f

from sqlalchemy.orm import sessionmaker

from .change_email import change_email, enter_new_email
from .change_phone import change_phone, enter_new_phone
from .change_fullname import change_fullname, enter_new_fullname
from .register import register, enter_fullname, enter_email, enter_phone_number, resend_otp, confirm_otp
from .start import start_registered, start_unregistered
from .profile_menu import profile_menu

from telegram_bot.filters import IsRegistered
from telegram_bot.states import Register, UserState, AdminState, OwnerState


def register_common_handlers(router: Router, session_pool: sessionmaker) -> None:
    router.message.register(start_unregistered, CommandStart(), ~IsRegistered(session_pool))
    router.message.register(start_registered, CommandStart(), IsRegistered(session_pool))
    router.message.register(enter_new_email, IsRegistered(session_pool), UserState.change_email)

    router.message.register(enter_fullname, Register.enter_fullname)
    router.message.register(enter_phone_number, Register.enter_phone_number)
    router.message.register(enter_email, Register.enter_email)
    router.message.register(confirm_otp, Register.confirm_otp)
    router.message.register(enter_new_fullname, IsRegistered(session_pool), UserState.change_fullname)
    router.message.register(enter_new_phone, IsRegistered(session_pool), UserState.change_phone_number)

    router.callback_query.register(change_phone, IsRegistered(session_pool), F.data == 'change_phone_number', UserState.profile_menu)
    router.callback_query.register(change_fullname, IsRegistered(session_pool), F.data == 'change_fullname', UserState.profile_menu)
    router.callback_query.register(change_email, IsRegistered(session_pool), F.data == 'change_email', UserState.profile_menu)

    router.callback_query.register(
        profile_menu,
        IsRegistered(session_pool),
        F.data == 'profile_menu',
        or_f(
            UserState.main_menu,
            AdminState.main_menu,
            OwnerState.main_menu
        ))

    router.callback_query.register(register, F.data == 'register')
    router.callback_query.register(resend_otp, Register.resend_otp)
