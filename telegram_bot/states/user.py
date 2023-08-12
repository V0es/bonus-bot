from aiogram.fsm.state import State, StatesGroup


class UserState(StatesGroup):

    main_menu = State()
    profile_menu = State()
