from aiogram import Router, F
from aiogram.filters import CommandStart
from .change_email import change_email
from .change_phone import change_phone
from .login import login
from .register import register, enter_fullname, enter_email, enter_phone_number, resend_otp, confirm_otp
from .start import start

from states import Register


def register_common_commands(router: Router) -> None:
    router.message.register(start, CommandStart())
    router.callback_query.register(register, F.data == 'register')
    router.message.register(enter_fullname, Register.enter_fullname)
    router.message.register(enter_phone_number, Register.enter_phone_number)
    router.message.register(enter_email, Register.enter_email)
    router.callback_query.register(resend_otp, Register.resend_otp)
    router.message.register(confirm_otp, Register.confirm_otp)
    
