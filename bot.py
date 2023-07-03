from aiogram import Bot, Dispatcher, types, executor
from config import Telegram
from db.commands import db
from chat_gpt_request import requests_gpt


bot = Bot(Telegram.api_key)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start'])
async def create_user(message):
    await db.create_user(message.from_user.id, message.from_user.username)
    await bot.send_message(message.from_user.id, f'ИДИ НАХУЙ, @{message.from_user.username}!')


@dp.message_handler(content_types=types.ContentType.TEXT)
async def process_message(message: types.Message):
    text = db.add_message(message.from_user.id, message.text, "user")
    print(f"text{text}")
    response = await requests_gpt(text)
    print(f"чresponse{response}")
    db.add_message(message.from_user.id, response, "assistant")
    await message.answer(response)


@dp.message_handler(content_types=types.ContentType.VOICE)
def process_voice_message(voice_message: types.Message):
    text = convert_to_text(voice_message.voice)
    db.add_message(message.from_user.id, text, "user")
    response = await requests_gpt(text)
    db.add_message(message.from_user.id, response, "assistant")
    await message.answer(response)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
