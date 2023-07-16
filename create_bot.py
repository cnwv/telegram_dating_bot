from aiogram import Dispatcher, Bot
from config import Telegram
from aiogram.contrib.fsm_storage.memory import MemoryStorage


storage: MemoryStorage = MemoryStorage()
bot: Bot = Bot(token=Telegram.api_key)
dp: Dispatcher = Dispatcher(bot, storage=storage)
