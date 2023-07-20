from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

inlineKb = InlineKeyboardMarkup(row_width=1).add(InlineKeyboardButton(text='Главное меню', callback_data='end_dialog'))
#for /start command
initial_data = InlineKeyboardMarkup(row_width=2)
block1 = InlineKeyboardButton(text='Знакомство в жизни', callback_data='life')
block2 = InlineKeyboardButton(text='Знакомство в сети', callback_data='online')
initial_data.row(block1, block2)

#life block
