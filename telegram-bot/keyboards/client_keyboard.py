from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

account_info_btn = InlineKeyboardButton(text='Количество баллов', callback_data='0')
change_phone_btn = InlineKeyboardButton(text='Сменить номер телефона', callback_data='0')
change_email_btn = InlineKeyboardButton(text='Сменить эл.почту', callback_data='0')

client_keyboard = InlineKeyboardMarkup(row_width=1)

client_keyboard.add(account_info_btn).add(change_phone_btn).add(change_email_btn)