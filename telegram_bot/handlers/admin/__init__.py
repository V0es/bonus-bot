from aiogram import Router, F
from sqlalchemy.orm import sessionmaker
from aiogram.filters import or_f

from telegram_bot.filters import IsAdmin, IsRegistered, IsOwner

from telegram_bot.states import AdminState, OwnerState

from .owner import add_admin
from .owner import remove_admin

from .add_order import add_order, enter_customer_number, enter_order_amount
from .export_database import export_database
from .set_account import set_account, enter_new_account

from .main_menu import admin_main_menu


def register_admin_handlers(router: Router, session_pool: sessionmaker) -> None:
    router.callback_query.register(
        admin_main_menu,
        IsAdmin(session_pool),
        ~IsOwner(session_pool),
        IsRegistered(session_pool),
        F.data == 'main_menu'
    )

    router.callback_query.register(
        add_order,
        IsRegistered(session_pool),
        IsAdmin(session_pool),
        or_f(
            AdminState.main_menu,
            OwnerState.main_menu
        ),
        F.data == 'add_order'
    )

    router.message.register(
        enter_customer_number,
        IsRegistered(session_pool),
        IsAdmin(session_pool),
        AdminState.enter_customer_number
    )

    router.message.register(
        enter_order_amount,
        IsRegistered(session_pool),
        IsAdmin(session_pool),
        AdminState.enter_order_amount
    )

    router.callback_query.register(
        export_database,
        IsRegistered(session_pool),
        IsAdmin(session_pool),
        or_f(
            AdminState.main_menu,
            OwnerState.main_menu
        ),
        F.data == 'export'
    )

    router.callback_query.register(
        set_account,
        IsRegistered(session_pool),
        IsAdmin(session_pool),
        or_f(
            AdminState.main_menu,
            OwnerState.main_menu
            ),
        F.data == 'set_account'
    )

    router.message.register(
        enter_new_account,
        IsRegistered(session_pool),
        IsAdmin(session_pool),
        AdminState.enter_new_account
    )
