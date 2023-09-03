from aiogram import Router, F
from aiogram.filters import invert_f

from sqlalchemy.orm import sessionmaker

from .main_menu import client_main_menu
from .account_info import account_info
from .promotions import promotions

from telegram_bot.filters import IsAdmin, IsRegistered, IsOwner

from telegram_bot.states import UserState


def register_client_handlers(router: Router, session_pool: sessionmaker) -> None:
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
