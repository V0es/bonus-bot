from aiogram import Router, F
from aiogram.filters import CommandStart, or_f


from sqlalchemy.orm import sessionmaker

from telegram_bot.filters import IsRegistered, IsAdmin, IsOwner
from telegram_bot.states import Register, UserState, AdminState, OwnerState

from telegram_bot.handlers.common.change_email import enter_new_email, change_email
from telegram_bot.handlers.common.change_fullname import enter_new_fullname, change_fullname
from telegram_bot.handlers.common.change_phone import enter_new_phone, change_phone
from telegram_bot.handlers.common.profile_menu import profile_menu
from telegram_bot.handlers.common.register import enter_fullname, enter_phone_number, enter_email, confirm_otp, \
    register, resend_otp
from telegram_bot.handlers.common.start import start_unregistered, start_registered

from telegram_bot.handlers.client.account_info import account_info
from telegram_bot.handlers.client.main_menu import client_main_menu
from telegram_bot.handlers.client.promotions import promotions

from telegram_bot.handlers.admin.add_order import enter_customer_number, enter_order_amount, add_order
from telegram_bot.handlers.admin.export_database import export_database
from telegram_bot.handlers.admin.main_menu import admin_main_menu
from telegram_bot.handlers.admin.set_account import enter_new_account, set_account

from telegram_bot.handlers.admin.owner.add_admin import add_admin
from telegram_bot.handlers.admin.owner.enter_admin_phone import enter_admin_phone
from telegram_bot.handlers.admin.owner.main_menu import owner_main_menu
from telegram_bot.handlers.admin.owner.remove_admin import remove_admin


def register_all_handlers(router: Router, session_pool: sessionmaker):
    _register_common_handlers(router, session_pool)
    _register_client_handlers(router, session_pool)
    _register_admin_handlers(router, session_pool)
    _register_owner_handlers(router, session_pool)


def _register_common_handlers(router: Router, session_pool: sessionmaker) -> None:
    router.message.register(start_unregistered, CommandStart(), ~IsRegistered(session_pool))
    router.message.register(start_registered, CommandStart(), IsRegistered(session_pool))
    router.message.register(enter_new_email, IsRegistered(session_pool), UserState.change_email)

    router.message.register(enter_fullname, Register.enter_fullname)
    router.message.register(enter_phone_number, Register.enter_phone_number)
    router.message.register(enter_email, Register.enter_email)
    router.message.register(confirm_otp, Register.confirm_otp)
    router.message.register(enter_new_fullname, IsRegistered(session_pool), UserState.change_fullname)
    router.message.register(enter_new_phone, IsRegistered(session_pool), UserState.change_phone_number)

    router.callback_query.register(
        change_phone,
        IsRegistered(session_pool),
        F.data == 'change_phone_number',
        UserState.profile_menu)

    router.callback_query.register(
        change_fullname,
        IsRegistered(session_pool),
        F.data == 'change_fullname',
        UserState.profile_menu)

    router.callback_query.register(
        change_email,
        IsRegistered(session_pool),
        F.data == 'change_email',
        UserState.profile_menu)

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


def _register_client_handlers(router: Router, session_pool: sessionmaker) -> None:
    router.callback_query.register(
        client_main_menu,
        ~IsAdmin(session_pool),
        ~IsOwner(session_pool),
        IsRegistered(session_pool),
        F.data == 'main_menu'
    )

    router.callback_query.register(
        account_info,
        IsRegistered(session_pool),
        UserState.main_menu,
        F.data == 'account_info'
    )

    router.callback_query.register(  # move text to separate file
        promotions,
        IsRegistered(session_pool),
        UserState.main_menu,
        F.data == 'promotions'
    )


def _register_admin_handlers(router: Router, session_pool: sessionmaker) -> None:
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


def _register_owner_handlers(router: Router, session_pool: sessionmaker) -> None:
    router.callback_query.register(
        owner_main_menu,
        IsRegistered(session_pool),
        IsOwner(session_pool),
        F.data == 'main_menu'
    )

    router.callback_query.register(
        add_admin,
        IsRegistered(session_pool),
        IsOwner(session_pool),
        F.data == 'add_admin'
    )

    router.callback_query.register(
        remove_admin,
        IsRegistered(session_pool),
        IsOwner(session_pool),
        F.data == 'remove_admin'
    )

    router.message.register(
        enter_admin_phone,
        IsRegistered(session_pool),
        IsOwner(session_pool),
        OwnerState.enter_admin_phone
    )
