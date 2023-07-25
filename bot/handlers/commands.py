from aiogram.types import ContentType

from bot.keyboards.inline_buttons import register_initial_buttons
from create_bot import bot, dp
from db.commands import db
from aiogram import Dispatcher
from aiogram import types
from config import Telegram
from aiogram.dispatcher import FSMContext


@dp.message_handler(commands=['start'])
async def create_user(message: types.Message):
    add_payment = not db.is_user_premium(message.from_user.id)
    db.create_user(message.from_user.id, message.from_user.username)
    await message.answer(f'{Telegram.start_text}', reply_markup=register_initial_buttons(add_payment=add_payment))


@dp.message_handler(commands=['restart'])
async def restart_command(message: types.Message, state: FSMContext):
    add_payment = not db.is_user_premium(message.from_user.id)
    db.delete_message(message.from_user.id)
    await state.finish()
    await message.answer("Бот перезагружен. Вы можете начать заново. Нажмите /start, чтобы начать новое знакомство",
                         reply_markup=register_initial_buttons(add_payment=add_payment))


async def help(message: types.Message):
    add_payment = not db.is_user_premium(message.from_user.id)
    await bot.send_message(message.from_user.id, f'{Telegram.start_text}',
                           reply_markup=register_initial_buttons(add_payment=add_payment))


@dp.callback_query_handler(text='end_dialog')
async def end_dialog(message: types.CallbackQuery):
    add_payment = not db.is_user_premium(message.from_user.id)
    db.delete_message(message.from_user.id)
    await bot.send_message(message.from_user.id,
                           'Хорошо, если у тебя больше нет вопросов или нужды в моей помощи, я закончу этот чат. '
                           'Если в будущем у тебя возникнут вопросы или нужна будет поддержка, не стесняйся обратиться. '
                           'Удачи в поиске любви и во всех твоих усилиях на пути к ней! Прощай!',
                           reply_markup=register_initial_buttons(add_payment=add_payment))
    await message.answer('Выбери знакомство')


@dp.callback_query_handler(text='payment')
async def payment(message: types.CallbackQuery):
    if Telegram.payment_key.split(':')[1] == 'TEST':
        await bot.send_message(message.from_user.id, text="Тестовый платеж!!!")
    price = types.LabeledPrice(label="Подписка", amount=500 * 100)  # в копейках (1 руб == 1 * 100)
    await bot.send_invoice(chat_id=message.from_user.id,
                           title="Подписка на бота",
                           description="Активация подписки на бота",
                           provider_token=Telegram.payment_key,
                           currency="RUB",
                           # photo_url="https://img.freepik.com/premium-vector/online-payment-concept_118813-2685.jpg",
                           # photo_width=605,
                           # photo_height=626,
                           # photo_size=15000,
                           is_flexible=False,
                           prices=[price],
                           start_parameter="subscription",
                           payload=str(message.from_user.id))


# pre checkout (must be answered in 10 seconds)
@dp.pre_checkout_query_handler(lambda query: True)
async def pre_checkout_query(pre_checkout_q: types.PreCheckoutQuery):
    await bot.answer_pre_checkout_query(pre_checkout_q.id, ok=True)


# successful payment
@dp.message_handler(content_types=ContentType.SUCCESSFUL_PAYMENT)
async def successful_payment(message: types.Message):
    payment_info = message.successful_payment.to_python()
    user_id = payment_info['invoice_payload']
    db.set_user_premium(id=user_id)
    print("successful payment for user with id: ", payment_info['invoice_payload'])
    await bot.send_message(message.chat.id,
                           f"Платеж на сумму {message.successful_payment.total_amount // 100} "
                           f"{message.successful_payment.currency} прошел успешно!")


def register_handlers_commands(dp: Dispatcher):
    dp.register_message_handler(help, commands=['help'])
