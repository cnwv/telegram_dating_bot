from bot.keyboards import register_end_dialog_button
from bot.keyboards.inline_buttons import register_subscribe_button
from bot.robokassa import generate_payment_link
from config import Robokassa, Telegram
from create_bot import dp, bot
from aiogram import types, Dispatcher
from db.commands import db
from utils.chat_gpt_request import RELATIONSHIP_STATE, OFFLINE_STATE, ONLINE_STATE, requests_gpt

OFFLINE_TEXT = 'Где ты находишься? Как выглядит субъект для знакомства? Что она или он делает? Девушка это или ' \
               'парень? Расскажи как можно больше подробностей – тогда ответ будет более точен.\n\n' \
               '<i><b>Например, напиши боту: "Хочу познакомиться с девушкой, ' \
               'она сидит в французском кафе в Санкт-Петербурге, пьет банановый капучино и читает книгу Рэя Брэдбери. ' \
               'Что ей сказать?".</b></i>'


# Первый блок для общения вживую
@dp.callback_query_handler(text='offline')
async def offline_state_handler(message: types.CallbackQuery):
    await message.message.answer(
        OFFLINE_TEXT, parse_mode="html"
    )
    print('Нажата кнопка - life')
    db.add_type_of_relationship(message.from_user.id, OFFLINE_STATE)


ONLINE_TEXT = 'Хочешь начать общение или продолжить? Какие увлечения у субъекта твоего интереса? ' \
              'Девушка это или парень? Расскажи всё, что поможет подойти к ответу наиболее конкретно.\n\n' \
              '<i><b>Например, напиши боту: "Хочу начать общение с девушкой, она любит настольный теннис и вечеринки, ' \
              'а ещё слушает электронную музыку и живёт в Санкт-Петербурге. Что ей написать?" ' \
              'или продолжи разговор уже начатый: "Что ответить на «Привет, как дела»?".</b></i>'


# Второй блок для общения по сети
@dp.callback_query_handler(text='online')
async def online_state_handler(message: types.CallbackQuery):
    await message.message.answer(
        ONLINE_TEXT, parse_mode="html"
    )
    print('Нажата кнопка - online')
    db.add_type_of_relationship(message.from_user.id, ONLINE_STATE)


RELATIONSHIP_TEXT = 'Напишите, какие проблемы во взаимоотношениях Вас беспокоят?\n\n' \
                    '<i><b>Например, напишите боту: "Как корректно расстаться с парнем, ' \
                    'с которым мы встречаемся уже 4 года из-за его инфантильности?" или ' \
                    '"Как правильно поддержать человека в трудную минуту?"</b></i>'


# Третий блок для взаимоотношений
@dp.callback_query_handler(text='relationship')
async def relationship_state_handler(message: types.CallbackQuery):
    await message.message.answer(
        RELATIONSHIP_TEXT, parse_mode="html"
    )
    print('Нажата кнопка - relationship')
    db.add_type_of_relationship(message.from_user.id, RELATIONSHIP_STATE)


@dp.callback_query_handler(text='another_choice')
async def another_choice_handler(message: types.CallbackQuery):
    print('Нажата кнопка - another_choice')
    sticker = await bot.send_sticker(chat_id=message.from_user.id,
                                     sticker=r"CAACAgIAAxkBAAEJk11ko1ef60EMUUHgRUS9der_oBAmlwACIwADKA9qFCdRJeeMIKQGLwQ")
    response = await requests_gpt(id=message.from_user.id, another_choice=True, text="Сгенерируй другой вариант.")
    await bot.delete_message(chat_id=message.from_user.id, message_id=sticker.message_id)
    await message.bot.send_message(chat_id=message.from_user.id, text=response,
                                   reply_markup=register_end_dialog_button(dialog=True))


SUBSCRIBE_TEXT = 'Нажимая кнопку ниже я даю согласие на обработку персональных данных и ' \
                 'принимаю условия <a href="https://supervespa.ru/heartmatebot">публичной оферты</a>.'


# Блок подписки
@dp.callback_query_handler(text='subscribe')
async def choose_subscribe_handler(message: types.CallbackQuery):
    await message.message.answer(
        SUBSCRIBE_TEXT, parse_mode="html",
        reply_markup=register_subscribe_button()
    )
    print('Нажата кнопка - subscribe')


# Блок first_sub
@dp.callback_query_handler(lambda c: c.data.startswith('subscription:'))
async def subscribe_handler(message: types.CallbackQuery):
    callback_data = message.data
    subscription = callback_data.split(':')[1]

    if subscription == 'day':
        cost = 149
    elif subscription == 'month':
        cost = 399
    elif subscription == 'year':
        cost = 1999
    else:
        await bot.send_message(message.from_user.id,
                               text="wrong data")
    password = Robokassa.password_1 if not Telegram.debug else Robokassa.test_password_1
    payment_link = generate_payment_link(merchant_login="heartbot",
                                         merchant_password_1=password,
                                         cost=cost,
                                         number=message.from_user.id,
                                         description=f"Подписка на бота",
                                         is_test=Telegram.debug)
    await bot.send_message(message.from_user.id,
                           text=payment_link)


def register_handlers_callbacks(dpt: Dispatcher):
    dpt.register_callback_query_handler(offline_state_handler, text='offline')
    dpt.register_callback_query_handler(online_state_handler, text='online')
    dpt.register_callback_query_handler(relationship_state_handler, text='relationship')
    dpt.register_callback_query_handler(another_choice_handler, text='another_choice')
    dpt.register_callback_query_handler(choose_subscribe_handler, text='subscribe')
    dpt.register_callback_query_handler(subscribe_handler)
