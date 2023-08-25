from aiogram.fsm.state import State, StatesGroup


class AdminState(StatesGroup):

    main_menu = State()
    add_order = State()
    change_bonuses = State()
    enter_customer_number = State()
    enter_order_amount = State()
    set_account = State()
    enter_new_account = State()
    export = State()
