from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def get_client_mainmenu_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(row_width=1, inline_keyboard=[
        [
            InlineKeyboardButton(text='Мой профиль', callback_data='profile_menu'),
            InlineKeyboardButton(text='Мои баллы', callback_data='account_info'),
            InlineKeyboardButton(text='Акции', callback_data='promotions'),
            InlineKeyboardButton(text='Связаться со службой поддержки(пока в разработке)', callback_data='0')
        ]
    ])
