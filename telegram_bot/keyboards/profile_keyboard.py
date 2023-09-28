from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def get_profile_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text='Изменить телефон', callback_data='change_phone_number')
            ],
            [
                InlineKeyboardButton(text='Изменить имя', callback_data='change_fullname')
            ],
            [
                InlineKeyboardButton(text='Изменить email', callback_data='change_email')
            ],
            [
                InlineKeyboardButton(text='Вернуться в главное меню', callback_data='main_menu')
            ]
        ]
    )
