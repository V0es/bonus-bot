from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def get_admin_mainmenu_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(row_width=1, inline_keyboard=[
        [
            InlineKeyboardButton(text='Мой профиль', callback_data='profile_menu'),
        ],
        [
            InlineKeyboardButton(text='Добавить заказ', callback_data='add_order'),
        ],
        [
            InlineKeyboardButton(text='Изменить баллы', callback_data='set_account'),
        ],
        [
            InlineKeyboardButton(text='Экспорт в Excel', callback_data='export')
        ]
        
    ])
