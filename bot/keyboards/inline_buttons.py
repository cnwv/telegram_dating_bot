from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def register_end_dialog_button(add_payment=False):
    inline_keyboard = InlineKeyboardMarkup(row_width=1).add(
        InlineKeyboardButton(text='Другой вариант', callback_data='another_choice'),
        InlineKeyboardButton(text='Главное меню', callback_data='end_dialog'),
    )
    if add_payment:
        if add_payment:
            payment_button = InlineKeyboardButton(text='Оплата', callback_data='payment')
            inline_keyboard.add(payment_button)
    return inline_keyboard


# for /start command
def register_initial_buttons(add_payment=False):
    initial_data = InlineKeyboardMarkup(row_width=2)
    block1 = InlineKeyboardButton(text='Знакомство в жизни', callback_data='offline')
    block2 = InlineKeyboardButton(text='Знакомство в сети', callback_data='online')
    block3 = InlineKeyboardButton(text='Взаимоотношения', callback_data='relationship')
    initial_data.row(block1, block2)
    initial_data.row(block3)
    if add_payment:
        payment_button = InlineKeyboardButton(text='Оплата', callback_data='payment')
        initial_data.add(payment_button)
    return initial_data
