from aiogram import Router, F

from sqlalchemy.orm import sessionmaker

from .main_menu import main_menu
from filters import IsAdmin, IsRegistered

from states import UserState


def register_client_handlers(router: Router, session_pool: sessionmaker) -> None:
    router.callback_query.register(main_menu,
                                   ~IsAdmin(session_pool),
                                   IsRegistered(session_pool),
                                   F.data == 'main_menu')
    print('REGISTERED MAIN MENU HANDLER')
