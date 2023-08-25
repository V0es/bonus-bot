from aiogram.fsm.state import State, StatesGroup


class OwnerState(StatesGroup):

    main_menu = State()
    add_admin = State()
    remove_admin = State()
    enter_admin_phone = State()
