from aiogram.fsm.state import State, StatesGroup


class Register(StatesGroup):

    enter_fullname = State()
    enter_phone_number = State()
    enter_email = State()
    confirm_otp = State()
    resend_otp = State()
