from aiogram import Router, F

from sqlalchemy.orm import sessionmaker

from .main_menu import main_menu
from .account_info import account_info
from .promotions import promotions

from filters import IsAdmin, IsRegistered

from states import UserState


def register_client_handlers(router: Router, session_pool: sessionmaker) -> None:
    router.callback_query.register(
        main_menu,
        ~IsAdmin(session_pool),
        IsRegistered(session_pool),
        F.data == 'main_menu'
    )
    
    router.callback_query.register(
        account_info,
        IsRegistered(session_pool),
        UserState.main_menu,
        F.data == 'account_info'
    )

    router.callback_query.register(  # move text to sepatate file and add filter for admins
        promotions,
        IsRegistered(session_pool),
        UserState.main_menu,
        F.data == 'promotions'
    )
