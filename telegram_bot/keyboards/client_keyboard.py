from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

account_info_btn = InlineKeyboardButton(text='Количество баллов', callback_data='0')
change_phone_btn = InlineKeyboardButton(text='Сменить номер телефона', callback_data='0')
change_email_btn = InlineKeyboardButton(text='Сменить эл.почту', callback_data='0')

client_keyboard = InlineKeyboardMarkup(row_width=1, inline_keyboard=[[account_info_btn, change_phone_btn, change_email_btn]])
