from aiogram import executor
from create_bot import dp
from bot.handlers import commands, initial_handlers, messages


async def on_startup(_):
    print('The bot is up and running.')


def main():
    """
    Entrypoint function
    """
    commands.register_handlers_commands(dp)
    messages.register_handlers_message(dp)
    initial_handlers.register_handlers_callbacks(dp)
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)


if __name__ == "__main__":
    main()
