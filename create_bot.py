from aiogram import Dispatcher, Bot
from config import Telegram


bot = Bot(token=Telegram.api_key)
dp = Dispatcher(bot)