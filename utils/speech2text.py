#!/usr/bin/env python3
import json
import wave
from pydub import AudioSegment
from vosk import Model, KaldiRecognizer, SetLogLevel
from aiogram import types, bot
import pathlib
import aiofiles
import asyncio


SetLogLevel(-1)

WORKDIR = str(pathlib.Path(__file__).parent.absolute())


async def convert_to_wav(path):
    print(12334)
    # with open(path, 'rb') as file:
    #     audio = AudioSegment.from_ogg(file)
    #     audio.export('voice.wav', format='wav')
    #     print(audio)


async def speech2text(voice_message: types.Message):
    file = await bot.get_file


async def download_file(voice_message: types.Message):
    print(f'Мы тут - {voice_message}')
    file_path = WORKDIR + "/" + str(voice_message.message_id)
    file = asyncio.create_task(voice_message.voice.download(destination_file=file_path))
    await file
    convert_to_wav('test')


def speech2text_old(path_file):
    print('попали в метод')
    result = ''
    model = Model("vosk-model-small-ru-0.4")
    wf = wave.open('test1.wav', "rb")  # Тест
    # wf = wave.open(path_file, "rb")
    rec = KaldiRecognizer(model, wf.getframerate())
    while True:
        result = ''
        data = wf.readframes(16000)
        last_n = False
        if len(data) == 0:
            break
        if rec.AcceptWaveform(data):
            res = json.loads(rec.Result)
            print(rec.Result())
            if res['text'] != '':
                result += f"{res[res['text']]}"
                last_n = False
            elif not last_n:
                result += '\n'
                last_n = True
    res = json.loads(rec.FinalResult())
    result += f"{res['text']}"
    return result
