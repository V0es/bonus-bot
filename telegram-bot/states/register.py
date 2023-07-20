from aiogram.dispatcher.filters.state import StatesGroup, State


class Register(StatesGroup):

    enter_fullname = State()
    enter_phone_number = State()
    enter_email = State()
    confim_otp = State()
    resend_otp = State()
