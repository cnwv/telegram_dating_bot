import os

import wit
from pydub import AudioSegment

from config import Telegram
from create_bot import bot
from utils.chat_gpt_request import requests_gpt
from aiogram import types, Dispatcher
from bot.keyboards import register_end_dialog_button
import pathlib

WORKDIR = str(pathlib.Path(__file__).parent.absolute())


async def process_message(message: types.Message):
    sticker = await bot.send_sticker(chat_id=message.from_user.id,
                                     sticker=r"CAACAgIAAxkBAAEJk11ko1ef60EMUUHgRUS9der_oBAmlwACIwADKA9qFCdRJeeMIKQGLwQ")
    response = await requests_gpt(message.text, message.from_user.id, message.from_user.username)
    await bot.delete_message(chat_id=message.from_user.id, message_id=sticker.message_id)
    await message.answer(response,
                         reply_markup=register_end_dialog_button(
                             dialog=True if response != Telegram.expire_text else False))


wit_client = wit.Wit(Telegram.wit_ai_token)
wit_client.message_language = 'ru'


async def process_voice_message(message: types.Message):
    print("voice_message_handler")
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

        # Отправляем аудио на распознавание в Wit.ai
        with open(wav_audio_path, "rb") as audio_file:
            response = wit_client.speech(audio_file, headers={'Content-Type': 'audio/wav', 'Content-Language': 'ru'})

        os.remove(ogg_audio_path)
        os.remove(wav_audio_path)

        recognized_text = response['text']

        await message.reply(f"Распознанный текст: {recognized_text}")
        sticker = await bot.send_sticker(chat_id=message.from_user.id,
                                         sticker=r"CAACAgIAAxkBAAEJk11ko1ef60EMUUHgRUS9der_oBAmlwACIwADKA9qFCdRJeeMIKQGLwQ")
        response_gpt = await requests_gpt(recognized_text, message.from_user.id, message.from_user.username)
        await bot.delete_message(chat_id=message.from_user.id, message_id=sticker.message_id)
        await message.answer(response_gpt,
                             reply_markup=register_end_dialog_button(
                                 dialog=True if response_gpt != Telegram.expire_text else False))
    except Exception as e:
        print("Error in process_voice_message:", e)
        await message.reply("Ошибка при распозновании голоса")


def register_handlers_message(dp: Dispatcher):
    dp.register_message_handler(process_message, content_types=types.ContentType.TEXT)
    dp.register_message_handler(process_voice_message, content_types=types.ContentType.VOICE)
