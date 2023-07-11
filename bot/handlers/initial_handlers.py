from create_bot import bot, dp
from aiogram import types, Dispatcher
from utils.chat_gpt_request import requests_gpt
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from db.commands import db
from bot.keyboards import inlineKb


class offline_date_fields(StatesGroup):
    info = State()


class online_date_fields(StatesGroup):
    info = State()


# Вопрос-ответ на первый вопрос
is_online = ['Вопрос:Знакомство по сети или вживую? Ответ: вживую ',
             'Вопрос:Знакомство по сети или вживую? Ответ: Знакомство по сети']


# Первый блок для общения вживую
# @dp.callback_query_handler(text='life')
async def state_machine_start(message: types.CallbackQuery):
    await offline_date_fields.info.set()
    await message.message.answer(
        'Где ты находишься? Как выглядит субъект для знакомства? Что она или он делает? Девушка это или парень? Расскажи как можно больше подробностей?')


# @dp.message_handler(content_types=types.ContentType.TEXT, state=offline_date_fields.info)
async def load_appearance(message: types.Message, state: FSMContext):
    form = ''
    async with state.proxy() as data:
        data[0] = f"{is_online[0]}Вопрос: Как выглядит субъект для знакомства? Что она или он делает? Девушка это или парень? " \
                  f"Расскажи как можно больше подробностей? Ответ: {message.text}"
        data_dict = dict(data)
        form += data_dict[0]
        await message.answer(form)
        sticker = await bot.send_sticker(chat_id=message.from_user.id,
                                         sticker=r"CAACAgIAAxkBAAEJk11ko1ef60EMUUHgRUS9der_oBAmlwACIwADKA9qFCdRJeeMIKQGLwQ")
        text = db.add_message(message.from_user.id, form, "user")
        response = await requests_gpt(text)
        await bot.delete_message(chat_id=message.from_user.id, message_id=sticker.message_id)
        db.add_message(message.from_user.id, response, "assistant")
        await message.answer(response, reply_markup=inlineKb)
    await state.finish()


# Второй блок для общения по сети
# @dp.callback_query_handler(text='online')
async def state_machine_start_(message: types.CallbackQuery):
    await online_date_fields.info.set()
    await message.message.answer('Хочешь начать общение или продолжить? Какие увлечения у субъекта твоего интереса? '
                                 'Девушка это или парень? Расскажи всё, что поможет подойти к ответу наиболее конкретно')


# @dp.message_handler(content_types=types.ContentType.TEXT, state=online_date_fields.info)
async def load_status(message: types.Message, state: FSMContext):
    form = ''
    async with state.proxy() as data:
        data[0] = f'{is_online} Вопрос: Хочешь начать общение или продолжить? ' \
                  f'Какие увлечения у субъекта твоего интереса? ' \
                  f'Девушка это или парень? ' \
                  f'Расскажи всё, что поможет подойти к ответу наиболее конкретно  Ответ: {message.text}'
        data_dict = dict(data)
        form += data_dict[0]
        sticker = await bot.send_sticker(chat_id=message.from_user.id,
                                         sticker=r"CAACAgIAAxkBAAEJk11ko1ef60EMUUHgRUS9der_oBAmlwACIwADKA9qFCdRJeeMIKQGLwQ")
        text = db.add_message(message.from_user.id, form, "user")
        response = await requests_gpt(text)
        await bot.delete_message(chat_id=message.from_user.id, message_id=sticker.message_id)
        db.add_message(message.from_user.id, response, "assistant")
        await message.answer(response, reply_markup=inlineKb)
    await state.finish()


def register_handlers_callbacks(dp: Dispatcher):
    dp.register_callback_query_handler(state_machine_start, text='life')
    dp.register_callback_query_handler(state_machine_start_, text='online')
    dp.register_message_handler(load_status, content_types=types.ContentType.TEXT, state=online_date_fields.info)
    dp.register_message_handler(load_appearance, content_types=types.ContentType.TEXT, state=offline_date_fields.info)