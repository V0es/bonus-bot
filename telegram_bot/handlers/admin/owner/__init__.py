from aiogram import Router, F
from aiogram.filters import or_f
from sqlalchemy.orm import sessionmaker

from .add_admin import add_admin
from .remove_admin import remove_admin
from .main_menu import owner_main_menu
from .enter_admin_phone import enter_admin_phone

from telegram_bot.filters import IsOwner, IsRegistered
from telegram_bot.states import OwnerState


def register_owner_handlers(router: Router, session_pool: sessionmaker):
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
