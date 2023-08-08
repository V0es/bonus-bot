from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

kb1 = KeyboardButton('кнопка1')
kb2 = KeyboardButton('кнопка2')

kbm = ReplyKeyboardMarkup().add(kb1).add(kb2)
