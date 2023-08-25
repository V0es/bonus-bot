from aiogram.fsm.state import State, StatesGroup


class UserState(StatesGroup):

    main_menu = State()
    profile_menu = State()
    change_email = State()
    change_phone_number = State()
    change_fullname = State()
