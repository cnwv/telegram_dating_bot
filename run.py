from aiogram import executor, types
from create_bot import dp, app, webhook_path, bot
from config import Telegram
from aiohttp import web


async def set_webhook():
    webhook_uri = f'https://5644-2a0b-6204-41fa-9000-986b-16b5-53dd-85c2.ngrok-free.app{webhook_path}'
    await bot.set_webhook(
        webhook_uri
    )


async def handle_webhook(request):
    url = str(request.url)
    index = url.rfind('/')
    token = url[index + 1:]

    if token == Telegram.api_key:
        request_data = await request.json()
        update = types.Update(**request_data)
        await dp.process_update(update)
        return web.Response()
    else:
        return web.Response(status=403)


app.router.add_post(f'/{Telegram.api_key}', handle_webhook)


async def on_startup(_):
    await set_webhook()
    print('The bot is up and running.')


from bot.handlers import commands, initial_handlers, messages

commands.register_handlers_commands(dp)
initial_handlers.register_handlers_callbacks(dp)
messages.register_handlers_message(dp)

if __name__ == '__main__':
    app.on_startup.append(on_startup)
    web.run_app(
        app,
        host='0.0.0.0',
        port=8080,
    )
