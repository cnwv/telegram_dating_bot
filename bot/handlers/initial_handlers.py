from create_bot import bot, dp
from aiogram import types, Dispatcher
from utils.chat_gpt_request import requests_gpt
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from db.commands import db
from bot.keyboards import inlineKb


class offline_date_fields(StatesGroup):
    location = State()
    appearance = State()
    hobby = State()
    other_info = State()


class online_date_fields(StatesGroup):
    status = State()
    hobby = State()
    sex = State()


# Вопрос-ответ на первый вопрос
is_online = ['1.Знакомство по сети или вживую? Ответ: вживую ',
             '1.Знакомство по сети или вживую? Ответ: Знакомство по сети']


# Первый блок для общения вживую
@dp.callback_query_handler(text='life')
async def state_machine_start(message: types.CallbackQuery):
    await offline_date_fields.location.set()
    await message.message.answer('Где ты находишься?')


# Первый,второй вопрос
@dp.message_handler(content_types=types.ContentType.TEXT, state=offline_date_fields.location)
async def load_location(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data[12] = f'{is_online[0]}2.Где ты находишься? Ответ:{message.text}'
    await offline_date_fields.next()
    await message.reply('Как выглядит субъект для знакомства?')


# Третий вопрос
@dp.message_handler(content_types=types.ContentType.TEXT, state=offline_date_fields.appearance)
async def load_appearance(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data[3] = f"3.Как выглядит субъект для знакомства? Ответ:{message.text}"
    await offline_date_fields.next()
    await message.reply('Что она или он делает?')


# Четвертый вопрос
@dp.message_handler(content_types=types.ContentType.TEXT, state=offline_date_fields.hobby)
async def load_appearance(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data[4] = f"4.Что она или он делает? Ответ:{message.text}"
    await offline_date_fields.next()
    await message.reply('Расскажи подробности')


# Пятый вопрос
@dp.message_handler(content_types=types.ContentType.TEXT, state=offline_date_fields.other_info)
async def load_appearance(message: types.Message, state: FSMContext):
    form = ''
    async with state.proxy() as data:
        data[4] = f"5.Расскажи подробности Ответ:{message.text}"
        data_dict = dict(data)
        for item in data_dict.values():
            form += item
        sticker = await bot.send_sticker(chat_id=message.from_user.id,
                                         sticker=r"CAACAgIAAxkBAAEJk11ko1ef60EMUUHgRUS9der_oBAmlwACIwADKA9qFCdRJeeMIKQGLwQ")
        text = db.add_message(message.from_user.id, form, "user")
        response = await requests_gpt(text)
        await bot.delete_message(chat_id=message.from_user.id, message_id=sticker.message_id)
        db.add_message(message.from_user.id, response, "assistant")
        await message.answer(response, reply_markup=inlineKb)
    await state.finish()


# Второй блок для общения по сети
@dp.callback_query_handler(text='online')
async def state_machine_start_(message: types.CallbackQuery):
    await online_date_fields.status.set()
    await message.message.answer('Хочешь начать общение или продолжить?')


# Первый, второй вопрос
@dp.message_handler(content_types=types.ContentType.TEXT, state=online_date_fields.status)
async def load_status(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data[12] = f'{is_online[1]}2.Хочешь начать общение или продолжить? Ответ:{message.text}'
    await online_date_fields.next()
    await message.reply('Какие увлечения?')


# Третий вопрос
@dp.message_handler(content_types=types.ContentType.TEXT, state=online_date_fields.hobby)
async def load_status(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data[3] = f' 3.Какие увлечения? Ответ:{message.text}'
    await online_date_fields.next()
    await message.reply('Девушка это или парень?')


# Четвертый вопрос
@dp.message_handler(content_types=types.ContentType.TEXT, state=online_date_fields.sex)
async def load_status(message: types.Message, state: FSMContext):
    form = ''
    async with state.proxy() as data:
        data[4] = f'4.Девушка это или парень? Ответ:{message.text}'
        data_dict = dict(data)
        for item in data_dict.values():
            form += item
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
