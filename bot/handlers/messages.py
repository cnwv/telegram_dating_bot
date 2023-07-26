from config import Telegram
from create_bot import bot
from utils.chat_gpt_request import requests_gpt
from aiogram import types, Dispatcher
from bot.keyboards import register_end_dialog_button
import pathlib

WORKDIR = str(pathlib.Path(__file__).parent.absolute())


async def process_message(message: types.Message):
    sticker = await bot.send_sticker(chat_id=message.from_user.id,
                                     sticker=r"CAACAgIAAxkBAAEJk11ko1ef60EMUUHgRUS9der_oBAmlwACIwADKA9qFCdRJeeMIKQGLwQ")
    response = await requests_gpt(message.text, message.from_user.id, message.from_user.username)
    await bot.delete_message(chat_id=message.from_user.id, message_id=sticker.message_id)
    await message.answer(response,
                         reply_markup=register_end_dialog_button(add_payment=False))


async def process_voice_message(message: types.Message):
    await message.answer('Я понимаю только текст.')
    # message_file = message.voice
    # downpath = WORKDIR + "/" + message_file.file_unique_id
    # await bot.download(file=message_file, destination=downpath)


def register_handlers_message(dp: Dispatcher):
    dp.register_message_handler(process_message, content_types=types.ContentType.TEXT)
    dp.register_message_handler(process_voice_message, content_types=types.ContentType.VOICE)
