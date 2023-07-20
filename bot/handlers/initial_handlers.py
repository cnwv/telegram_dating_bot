from create_bot import dp
from aiogram import types, Dispatcher
from db.commands import db


# Первый блок для общения вживую
@dp.callback_query_handler(text='life')
async def state_machine_start(message: types.CallbackQuery):
    await message.message.answer(
        f'Где ты находишься? Как выглядит субъект для знакомства? Что она или он делает? Девушка это или парень? '
        f'Расскажи как можно больше подробностей – тогда ответ будет более точен.\n\n'
        f'Например, напиши боту: "Хочу познакомиться с девушкой, она сидит в французском кафе в Санкт-Петербурге, '
        f'пьет банановый капучино и читает книгу Рэя Брэдбери. Что ей сказать?".'
    )
    print('Нажата кнопка - life')
    db.add_type_of_relationship(message.from_user.id, False)


# Второй блок для общения по сети
@dp.callback_query_handler(text='online')
async def state_machine_start_(message: types.CallbackQuery):
    await message.message.answer(
        f'Хочешь начать общение или продолжить? Какие увлечения у субъекта твоего интереса? Девушка это или парень? '
        f'Расскажи всё, что поможет подойти к ответу наиболее конкретно.\n\n'
        f'Например, напиши боту: "Хочу начать общение с девушкой, она любит настольный теннис и вечеринки, '
        f'а ещё слушает электронную музыку и живёт в Санкт-Петербурге. Что ей написать?" '
        f'или продолжи разговор уже начатый: "Что ответить на «Привет, как дела»?".'
    )
    print('Нажата кнопка - online')
    db.add_type_of_relationship(message.from_user.id, True)


def register_handlers_callbacks(dpt: Dispatcher):
    dpt.register_callback_query_handler(state_machine_start, text='life')
    dpt.register_callback_query_handler(state_machine_start_, text='online')
