from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


register_btn = InlineKeyboardButton(text='Зарегистирироваться', callback_data='register')

start_unregistered_keyboard = InlineKeyboardMarkup(row_width=1, inline_keyboard=[[register_btn]])


def get_unregistered_start_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(row_width=1, inline_keyboard=[
            [
                InlineKeyboardButton(text='Зарегистирироваться', callback_data='register')
            ]
        ])
    
    
def get_registered_start_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(row_width=1, inline_keyboard=[
        [
            InlineKeyboardButton(text='Войти в главное меню', callback_data='main_menu')
        ]
    ])
