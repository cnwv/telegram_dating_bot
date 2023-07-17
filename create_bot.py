from aiogram import Dispatcher, Bot
from config import Telegram
from aiohttp import web
from aiogram.contrib.middlewares.logging import LoggingMiddleware

bot = Bot(token=Telegram.api_key)
Bot.set_current(bot)
app = web.Application()
dp = Dispatcher(bot)
dp.middleware.setup(LoggingMiddleware())
webhook_path = f'/{Telegram.api_key}'
