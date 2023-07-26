from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def register_end_dialog_button(payment=False):
    inline_keyboard = InlineKeyboardMarkup(row_width=1)
    if not payment:
        inline_keyboard.add(InlineKeyboardButton(text='Другой вариант', callback_data='another_choice'))

    inline_keyboard.add(InlineKeyboardButton(text='Главное меню', callback_data='end_dialog'))
    return inline_keyboard


# for /start command
def register_initial_buttons():
    initial_data = InlineKeyboardMarkup(row_width=2)
    block1 = InlineKeyboardButton(text='Знакомство в жизни', callback_data='offline')
    block2 = InlineKeyboardButton(text='Знакомство в сети', callback_data='online')
    block3 = InlineKeyboardButton(text='Взаимоотношения', callback_data='relationship')
    initial_data.row(block1, block2)
    initial_data.row(block3)
    return initial_data
