from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

login_btn = InlineKeyboardButton(text='Войти', callback_data='login')
register_btn = InlineKeyboardButton(text='Зарегистирироваться', callback_data='register')

start_keyboard = InlineKeyboardMarkup(row_width=1, inline_keyboard=[[login_btn, register_btn]])
