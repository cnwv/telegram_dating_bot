from aiogram import types

from bot.handlers import commands, initial_handlers, messages
from bot.robokassa import result_payment, check_success_payment
from create_bot import dp, app, bot
from config import Telegram, Ngrok
from aiohttp import web


async def set_webhook():
    debug = Telegram.debug
    if debug:
        url_prefix = Ngrok.url
    else:
        url_prefix = "telegram-dating-bot.ru"
    webhook_url = f'{url_prefix}/{Telegram.api_key}'
    await bot.set_webhook(webhook_url)


async def handle_bot_webhook(request):
    print('handle_bot_webhook')

    url = str(request.url)
    index = url.rfind('/')
    token = url[index + 1:]

    if token == Telegram.api_key:
        request_data = await request.json()
        print("request data", request_data)
        update = types.Update(**request_data)
        await dp.process_update(update)
        return web.Response()
    else:
        return web.Response(status=403)


async def handle_result_url(request):
    print('handle_result_url')
    req = await request.json()
    print("request data:", req)
    inv_id = result_payment("M92pU2DfcAl5hlyXo3WY", str(req))
    print(inv_id)
    return web.Response()


async def handle_success_url(request):
    print('handle_success_url')
    req = await request.json()
    print("request data:", req)
    st = check_success_payment("ZgOuH6WvrB3G7p2nRl8a", str(req))
    print(st)
    return web.Response()


app.router.add_post(f'/{Telegram.api_key}', handle_bot_webhook)
app.router.add_post(f'/result_url', handle_result_url)
app.router.add_post(f'/success_url', handle_success_url)


async def on_startup(_):
    await set_webhook()
    print('The bot is up and running.')


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
