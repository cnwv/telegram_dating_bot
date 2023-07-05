from aiogram import Dispatcher, Bot
from config import Telegram
from aiogram.contrib.fsm_storage.memory import MemoryStorage

storage = MemoryStorage()

bot = Bot(token=Telegram.api_key)
dp = Dispatcher(bot, storage=storage)
