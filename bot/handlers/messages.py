from create_bot import dp, bot
from utils.chat_gpt_request import requests_gpt
from aiogram import types, Dispatcher
from db.commands import db


# @dp.message_handler(content_types=types.ContentType.TEXT)
async def process_message(message: types.Message):
    sticker = await bot.send_sticker(chat_id=message.from_user.id, sticker=r"CAACAgIAAxkBAAEJk11ko1ef60EMUUHgRUS9der_oBAmlwACIwADKA9qFCdRJeeMIKQGLwQ")
    text = db.add_message(message.from_user.id, message.text, "user")
    print(f"text{text}")
    response = await requests_gpt(text)
    await bot.delete_message(chat_id=message.from_user.id, message_id=sticker.message_id)
    print(f"чresponse{response}")
    db.add_message(message.from_user.id, response, "assistant")
    await message.answer(response)


# @dp.message_handler(content_types=types.ContentType.VOICE)
# def process_voice_message(voice_message: types.Message):
#     text = convert_to_text(voice_message.voice)
#     db.add_message(message.from_user.id, text, "user")
#     response = await requests_gpt(text)
#     db.add_message(message.from_user.id, response, "assistant")
#     await message.answer(response)

def register_handlers_message(dp: Dispatcher):
    dp.register_message_handler(process_message, content_types=types.ContentType.TEXT)
