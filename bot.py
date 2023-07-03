from aiogram import Bot, Dispatcher, types, executor
from config import Telegram
from db.commands import db
bot = Bot(Telegram.api_key)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start'])
async def create_user(message):
    await db.create_user(message.from_user.id, message.from_user.username)
    await bot.send_message(message.from_user.id, f'ИДИ НАХУЙ, @{message.from_user.username}!')


@dp.message_handler()
async def messages(message: types.Message):
    await db.add_message(message.from_user.id, message.text, "user")
    response = 'Ответ'
    await db.add_message(message.from_user.id, response, "assistant")
    await message.answer(message.text)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)


