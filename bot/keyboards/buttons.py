from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


b1 = KeyboardButton('/help')

kb_client = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)

kb_client.add(b1)