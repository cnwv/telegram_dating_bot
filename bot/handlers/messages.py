from create_bot import dp, bot
from utils.chat_gpt_request import requests_gpt
from aiogram.types import File
from aiogram import types, Dispatcher
from db.commands import db
from bot.keyboards import inlineKb
import pathlib
from aiogram import Bot
from io import BytesIO

WORKDIR = str(pathlib.Path(__file__).parent.absolute())
print(WORKDIR)


# @dp.message_handler(content_types=types.ContentType.TEXT)
async def process_message(message: types.Message):
    sticker = await bot.send_sticker(chat_id=message.from_user.id,
                                     sticker=r"CAACAgIAAxkBAAEJk11ko1ef60EMUUHgRUS9der_oBAmlwACIwADKA9qFCdRJeeMIKQGLwQ")
    text = db.add_message(message.from_user.id, message.text, "user")
    response = await requests_gpt(text)
    # response = message.text - echo mod
    await bot.delete_message(chat_id=message.from_user.id, message_id=sticker.message_id)
    db.add_message(message.from_user.id, response, "assistant")
    await message.answer(response)#reply_markup=inlineKb


async def process_voice_message(message: types.Message):
    message_file = message.voice
    downpath = WORKDIR + "/" + message_file.file_unique_id
    await bot.download(file=message_file, destination=downpath)


def register_handlers_message(dp: Dispatcher):
    dp.register_message_handler(process_message, content_types=types.ContentType.TEXT)
    dp.register_message_handler(process_voice_message, content_types=types.ContentType.VOICE)
