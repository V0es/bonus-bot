from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

resend_otp = InlineKeyboardButton(text='Отправить пароль заново', callback_data='resend_otp')

confirm_otp_keyboard = InlineKeyboardMarkup().add(resend_otp)
