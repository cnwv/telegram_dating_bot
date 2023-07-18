from create_bot import bot, dp
from aiogram import types, Dispatcher
from utils.chat_gpt_request import requests_gpt
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from bot.keyboards import inlineKb
from db.commands import db


# Вопрос-ответ на первый вопрос
# is_online = ['Знакомство вживую. Подробности:',
#              'Знакомство по сети. Подробности:']


# Первый блок для общения вживую
@dp.callback_query_handler(text='life')
async def state_machine_start(message: types.CallbackQuery):
    await message.message.answer(
        f'Где ты находишься? Как выглядит субъект для знакомства? Что она или он делает? Девушка это или парень? '
        f'Расскажи как можно больше подробностей?\n\n'
        f'Например, напишите боту после выбора знакомства онлайн «Хочу начать общение с девушкой, она любит большой теннис и вечеринки, а ещё слушает хорошую музыку и живёт в Санкт Петербурге.Что ей написать?» В случае, если ответа умного бота вам не подходит, можете попросить сгенерировать новый с теми же вводными.')
    print('Нажата кнопка')
    db.add_type_of_relationship(message.from_user.id, False)


# Второй блок для общения по сети
@dp.callback_query_handler(text='online')
async def state_machine_start_(message: types.CallbackQuery):
    await message.message.answer(f'Хочешь начать общение или продолжить? Какие увлечения у субъекта твоего интереса? '
                                 f'Девушка это или парень? Расскажи всё, что поможет подойти к ответу наиболее конкретно\n\n'
                                 f'Например, напишите боту после выбора знакомства онлайн «Хочу начать общение с девушкой, '
                                 f'она любит большой теннис и вечеринки, а ещё слушает хорошую музыку и живёт в Санкт Петербурге.Что ей '
                                 f'написать?» В случае, если ответа умного бота вам не подходит, можете попросить сгенерировать новый с теми же вводными.')
    print('Нажата кнопка')

    db.add_type_of_relationship(message.from_user.id, True)


# @dp.message_handler(content_types=types.ContentType.TEXT, state=online_date_fields.info)
# async def load_status(message: types.Message, state: FSMContext):
#     form = ''
#     async with state.proxy() as data:
#         data[0] = f'{is_online[1]} {message.text}'
#         data_dict = dict(data)
#         print(data_dict[0])
#         sticker = await bot.send_sticker(chat_id=message.from_user.id,
#                                          sticker=r"CAACAgIAAxkBAAEJk11ko1ef60EMUUHgRUS9der_oBAmlwACIwADKA9qFCdRJeeMIKQGLwQ")
#         response = await requests_gpt(data_dict[0], message.from_user.id)
#         await bot.delete_message(chat_id=message.from_user.id, message_id=sticker.message_id)
#         await message.answer(response, reply_markup=inlineKb)
#     await state.finish()


def register_handlers_callbacks(dpt: Dispatcher):
    dpt.register_callback_query_handler(state_machine_start, text='life')
    dpt.register_callback_query_handler(state_machine_start_, text='online')
    # dpt.register_message_handler(load_status, content_types=types.ContentType.TEXT, state=online_date_fields.info)
    # dpt.register_message_handler(load_appearance, content_types=types.ContentType.TEXT, state=offline_date_fields.info)
