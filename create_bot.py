from aiogram import Dispatcher, Bot
from config import Telegram
from aiohttp import web
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.fsm_storage.redis import RedisStorage2
from aiogram.contrib.middlewares.logging import LoggingMiddleware


# storage = MemoryStorage()
storage = RedisStorage2(host='localhost', port=6379, db=0, prefix='bot')


bot = Bot(token=Telegram.api_key)
Bot.set_current(bot)
app = web.Application()
dp = Dispatcher(bot)
dp.middleware.setup(LoggingMiddleware())
webhook_path = f'/{Telegram.api_key}'
