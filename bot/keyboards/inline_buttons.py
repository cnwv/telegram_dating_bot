from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

inlineKb = InlineKeyboardMarkup(row_width=1).add(InlineKeyboardButton(text='Закончить чат', callback_data='end_dialog'))

initial_data = InlineKeyboardMarkup(row_width=2)
block1 = InlineKeyboardButton(text='Знакомство в жизни', callback_data='life')
block2 = InlineKeyboardButton(text='Знакомство в сети', callback_data='internet')
initial_data.row(block1, block2)

