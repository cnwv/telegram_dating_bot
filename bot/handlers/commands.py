from create_bot import bot, dp
from db.commands import db
from aiogram import Dispatcher
from bot.keyboards import kb_client, initial_data
from aiogram import types
from config import Telegram
from aiogram.dispatcher import FSMContext


@dp.message_handler(commands=['start'])
async def create_user(message: types.Message):
    db.create_user(message.from_user.id, message.from_user.username)

    await message.answer(f'{Telegram.start_text}', reply_markup=initial_data)


@dp.message_handler(commands=['restart'])
async def restart_command(message: types.Message, state: FSMContext):
    db.delete_message(message.from_user.id)
    await state.finish()
    await message.answer("Бот перезагружен. Вы можете начать заново. Нажмите /start, чтобы начать новое знакомство")


async def help(message: types.Message):
    await bot.send_message(message.from_user.id, f'{Telegram.start_text}!')


@dp.callback_query_handler(text='end_dialog')
async def end_dialog(message: types.CallbackQuery):
    db.delete_message(message.from_user.id)
    await bot.send_message(message.from_user.id,
                           'Хорошо, если у тебя больше нет вопросов или нужды в моей помощи, я закончу этот чат. Если в будущем у тебя возникнут вопросы или нужна будет поддержка, не стесняйся обратиться. Удачи в поиске любви и во всех твоих усилиях на пути к ней! Прощай!',
                           reply_markup=initial_data)
    await message.answer('Выбери знакомство')


def register_handlers_commands(dp: Dispatcher):
    dp.register_message_handler(help, commands=['help'])
