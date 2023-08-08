import asyncio

from aiogram import types

from bot.handlers import commands, initial_handlers, messages
from bot.keyboards import register_end_dialog_button
from bot.robokassa import result_payment, check_success_payment
from create_bot import dp, app, bot
from config import Telegram, Web, Robokassa
from aiohttp import web

from db.commands import db


async def set_webhook():
    url_prefix = Web.main_url  # Web.ngrok_url
    webhook_url = f'{url_prefix}/{Telegram.api_key}'
    await bot.set_webhook(webhook_url)


def parse_url(req):
    url = str(req.url)
    index = url.rfind('/')
    return url[index + 1:]


async def handler_bot_webhook(request):
    print('handler_bot_webhook')
    token = parse_url(request)
    if token == Telegram.api_key:
        request_data = await request.json()
        print(f"[request data: {request_data}]")
        update = types.Update(**request_data)
        await dp.process_update(update)
        return web.Response()
    else:
        print("wrong path/token")
        return web.Response(status=403)


async def handler_result_url(request):
    print('handler_result_url')
    path = parse_url(request)
    print(f"[request url path: {path}]")
    password = Robokassa.password_2 if not Telegram.debug else Robokassa.test_password_2
    response = result_payment(merchant_password_2=password, request=str(path))
    print("response:", response)
    return web.Response(text=response, status=200)


async def handler_success_url(request):
    print('handler_success_url')
    path = parse_url(request)
    print(f"[request url path: {path}]")
    password = Robokassa.password_1 if not Telegram.debug else Robokassa.test_password_1
    response, user_id, subscribe_expire_day = check_success_payment(merchant_password_1=password, request=str(path))
    response += f" Ваша подписка активна до: {str(subscribe_expire_day)}" if subscribe_expire_day is not None else ""
    await dp.bot.send_message(chat_id=user_id,
                              text=response,
                              reply_markup=register_end_dialog_button(dialog=False))
    return web.Response()


app.router.add_post(f'/{Telegram.api_key}', handler_bot_webhook)

app.router.add_get(f'/result_url', handler_result_url)
app.router.add_get(f'/success_url', handler_success_url)


async def start_worker():
    while True:
        # проверяем каждый час что премиум не закончился
        db.check_premium_expire_for_all_users()
        await asyncio.sleep(3600)


async def on_startup(_):
    await set_webhook()
    asyncio.create_task(start_worker())
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
