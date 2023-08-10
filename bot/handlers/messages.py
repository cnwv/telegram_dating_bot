import asyncio
import io

from pydub import AudioSegment

from config import Telegram
from create_bot import bot, dp
from utils.chat_gpt_request import requests_gpt
from aiogram import types, Dispatcher
from bot.keyboards import register_end_dialog_button
import pathlib
import speech_recognition as sr
from wit import Wit

WORKDIR = str(pathlib.Path(__file__).parent.absolute())


async def process_message(message: types.Message):
    sticker = await bot.send_sticker(chat_id=message.from_user.id,
                                     sticker=r"CAACAgIAAxkBAAEJk11ko1ef60EMUUHgRUS9der_oBAmlwACIwADKA9qFCdRJeeMIKQGLwQ")
    response = await requests_gpt(message.text, message.from_user.id, message.from_user.username)
    await bot.delete_message(chat_id=message.from_user.id, message_id=sticker.message_id)
    await message.answer(response,
                         reply_markup=register_end_dialog_button(
                             dialog=True if response != Telegram.expire_text else False))


WIT_AI_TOKEN = 'BTJ5FWE4DQKQ3QJTLLF7Z6LOVG2JDU33'


# @dp.message_handler(content_types=types.ContentTypes.VOICE)
async def process_voice_message(message: types.Message):
    wit_client = Wit(WIT_AI_TOKEN)
    try:
        # Получение информации о голосовом сообщении
        file_id = message.voice.file_id
        file_info = await bot.get_file(file_id)
        downloaded_file = await bot.download_file(file_info.file_path)

        # Сохранение аудио файла на диск в формате OGG
        ogg_audio_path = "audio.ogg"
        with open(ogg_audio_path, "wb") as f:
            f.write(downloaded_file.read())

        # Преобразование аудио в формат WAV
        wav_audio = AudioSegment.from_ogg(ogg_audio_path)
        wav_audio_path = "audio.wav"
        wav_audio.export(wav_audio_path, format="wav")

        # Создание объекта для распознавания речи
        recognizer = sr.Recognizer()

        # Распознавание речи с использованием библиотеки SpeechRecognition
        with sr.AudioFile(wav_audio_path) as source:
            audio_data = recognizer.record(source)
            recognized_text = await recognize_audio(recognizer, audio_data)

            # Отправляем распознанный текст в Wit.ai для дополнительного анализа
            response = wit_client.message(recognized_text)
            intent = response['intents'][0]['name']

            await message.reply(f"Распознанный текст: {recognized_text}\nИнтент: {intent}")
    except Exception as e:
        await message.answer(e)


async def recognize_audio(recognizer, audio_data):
    loop = asyncio.get_running_loop()
    return await loop.run_in_executor(None, recognizer.recognize_google, audio_data)


def register_handlers_message(dp: Dispatcher):
    dp.register_message_handler(process_message, content_types=types.ContentType.TEXT)
    dp.register_message_handler(process_voice_message, content_types=types.ContentType.VOICE)
