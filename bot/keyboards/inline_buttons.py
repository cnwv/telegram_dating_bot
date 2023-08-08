from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def register_end_dialog_button(dialog=True):
    inline_keyboard = InlineKeyboardMarkup(row_width=1)
    if dialog:
        inline_keyboard.add(InlineKeyboardButton(text='Другой вариант', callback_data='another_choice'))
    inline_keyboard.add(InlineKeyboardButton(text='Главное меню', callback_data='end_dialog'))
    return inline_keyboard


# for /start command
def register_initial_buttons(subscribe=False):
    initial_data = InlineKeyboardMarkup(row_width=2)
    block1 = InlineKeyboardButton(text='Знакомство в жизни', callback_data='offline')
    block2 = InlineKeyboardButton(text='Знакомство в сети', callback_data='online')
    block3 = InlineKeyboardButton(text='Взаимоотношения', callback_data='relationship')
    initial_data.row(block1, block2)
    initial_data.row(block3)
    if subscribe:
        payment_block = InlineKeyboardButton(text='Подписка', callback_data='subscribe')
        initial_data.add(payment_block)
    return initial_data


def register_subscribe_button():
    inline_keyboard = InlineKeyboardMarkup()
    inline_keyboard.add(InlineKeyboardButton(text='День — 149₽',  callback_data='subscription:day'))
    inline_keyboard.add(InlineKeyboardButton(text='Месяц — 399₽', callback_data='subscription:month'))
    inline_keyboard.add(InlineKeyboardButton(text='Год — 1999₽', callback_data='subscription:year'))
    return inline_keyboard
