from create_bot import bot, dp
from db.commands import db
from bot.keyboards import kb_client, initial_data
from aiogram import types


@dp.callback_query_handler(text='life')
async def life(message: types.CallbackQuery):
    await message.
    await message.answer('cocи')
