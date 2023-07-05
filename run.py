from aiogram import executor
from create_bot import dp


async def on_startup(_):
    print('The bot is up and running.')


from bot.handlers import commands, messages

commands.register_handlers_commands(dp)
messages.register_handlers_message(dp)



executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
