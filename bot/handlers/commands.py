from create_bot import bot
from db.commands import db
from aiogram import Dispatcher


# @dp.message_handler(commands=['start'])
async def create_user(message):
    db.create_user(message.from_user.id, message.from_user.username)
    await bot.send_message(message.from_user.id, f'ИДИ НАХУЙ, @{message.from_user.username}!')
    print('Зарегался')


def register_handlers_commands(dp: Dispatcher):
    dp.register_message_handler(create_user, commands=['start', 'help'])
