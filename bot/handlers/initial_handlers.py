from bot.keyboards import register_end_dialog_button
from create_bot import dp, bot
from aiogram import types, Dispatcher
from db.commands import db
from utils.chat_gpt_request import RELATIONSHIP_STATE, OFFLINE_STATE, ONLINE_STATE, requests_gpt


# Первый блок для общения вживую
@dp.callback_query_handler(text='offline')
async def offline_state_handler(message: types.CallbackQuery):
    await message.message.answer(
        f'Где ты находишься? Как выглядит субъект для знакомства? Что она или он делает? Девушка это или парень? '
        f'Расскажи как можно больше подробностей – тогда ответ будет более точен.\n\n'
        f'Например, напиши боту: "Хочу познакомиться с девушкой, она сидит в французском кафе в Санкт-Петербурге, '
        f'пьет банановый капучино и читает книгу Рэя Брэдбери. Что ей сказать?".'
    )
    print('Нажата кнопка - life')
    db.add_type_of_relationship(message.from_user.id, OFFLINE_STATE)


# Второй блок для общения по сети
@dp.callback_query_handler(text='online')
async def online_state_handler(message: types.CallbackQuery):
    await message.message.answer(
        f'Хочешь начать общение или продолжить? Какие увлечения у субъекта твоего интереса? Девушка это или парень? '
        f'Расскажи всё, что поможет подойти к ответу наиболее конкретно.\n\n'
        f'Например, напиши боту: "Хочу начать общение с девушкой, она любит настольный теннис и вечеринки, '
        f'а ещё слушает электронную музыку и живёт в Санкт-Петербурге. Что ей написать?" '
        f'или продолжи разговор уже начатый: "Что ответить на «Привет, как дела»?".'
    )
    print('Нажата кнопка - online')
    db.add_type_of_relationship(message.from_user.id, ONLINE_STATE)


# Третий блок для взаимоотношений
@dp.callback_query_handler(text='relationship')
async def relationship_state_handler(message: types.CallbackQuery):
    await message.message.answer(
        f'Напишите, какие проблемы во взаимоотношениях Вас беспокоят?\n\n'
        f'Например, напишите боту: "Как корректно расстаться с парнем, с которым мы встречаемся уже 4 года из-за его '
        f'инфантильности?" или "Как правильно поддержать человека в трудную минуту?"'
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
                                   reply_markup=register_end_dialog_button())


def register_handlers_callbacks(dpt: Dispatcher):
    dpt.register_callback_query_handler(offline_state_handler, text='offline')
    dpt.register_callback_query_handler(online_state_handler, text='online')
    dpt.register_callback_query_handler(relationship_state_handler, text='relationship')
    dpt.register_callback_query_handler(another_choice_handler, text='another_choice')
