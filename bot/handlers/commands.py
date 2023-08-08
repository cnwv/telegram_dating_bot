from bot.handlers.initial_handlers import SUBSCRIBE_TEXT
from bot.keyboards.inline_buttons import register_initial_buttons, register_subscribe_button
from create_bot import bot, dp
from db.commands import db
from aiogram import Dispatcher
from aiogram import types
from config import Telegram
from aiogram.dispatcher import FSMContext


@dp.message_handler(commands=['start'])
async def create_user(message: types.Message):
    is_premium = db.is_user_premium(id=message.from_user.id)
    db.create_user(message.from_user.id, message.from_user.username)
    await message.answer(f'{Telegram.start_text}', reply_markup=register_initial_buttons(subscribe=not is_premium))


@dp.message_handler(commands=['restart'])
async def restart_command(message: types.Message, state: FSMContext):
    db.delete_message(message.from_user.id)
    await state.finish()
    await message.answer("Бот перезагружен. Вы можете начать заново. Нажмите /start, чтобы начать новое знакомство")


async def help(message: types.Message):
    is_premium = db.is_user_premium(id=message.from_user.id)
    await bot.send_message(message.from_user.id, f'{Telegram.start_text}',
                           reply_markup=register_initial_buttons(subscribe=not is_premium))


@dp.callback_query_handler(text='end_dialog')
async def end_dialog(message: types.CallbackQuery):
    is_premium = db.is_user_premium(id=message.from_user.id)
    db.delete_message(message.from_user.id)
    await bot.send_message(message.from_user.id,
                           'Хорошо, если у тебя больше нет вопросов или нужды в моей помощи. '
                           'Если в будущем у тебя возникнут вопросы или нужна будет поддержка, '
                           'не стесняйся обратиться. Удачи в поиске любви и во всех твоих усилиях на пути к ней.',
                           reply_markup=register_initial_buttons(subscribe=not is_premium))
    await message.answer('Выбери знакомство')


@dp.message_handler(commands=['subscribe'])
async def payment(message: types.CallbackQuery):
    await message.bot.send_message(message.from_user.id,
                                   text=SUBSCRIBE_TEXT, parse_mode="html",
                                   reply_markup=register_subscribe_button())


def register_handlers_commands(dp: Dispatcher):
    dp.register_message_handler(help, commands=['help'])
