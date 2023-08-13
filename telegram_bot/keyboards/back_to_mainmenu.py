from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def get_back_to_main_menu_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text='Вернуться в главное меню', callback_data='main_menu')
            ]
        ]
    )
