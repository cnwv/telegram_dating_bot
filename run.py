from config import Telegram
from aiogram import Bot, Dispatcher, executor
from bot import user_registration

if __name__ == "__name__":

    bot = Bot(Telegram.api_key)
    dp = Dispatcher(bot)
    executor.start_polling(dp, skip_updates=True)


