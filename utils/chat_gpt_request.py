import openai
from config import OpenAI
import asyncio
from db.commands import db

apy_key_list = eval(OpenAI.api_key)


async def requests_gpt(text, id):
    api_key = apy_key_list.pop(0)
    openai.api_key = api_key
    apy_key_list.append(api_key)
    dialog = await db.add_message(id, text, "user")
    print(dialog)
    print('GPT request')
    completion = openai.ChatCompletion.create(model="gpt-3.5-turbo",
                                              messages=dialog, max_tokens=2000)
    response = completion.choices[0].message.content
    await db.add_message(id, response, 'assistant')
    return response


if __name__ == '__main__':
    async def main():
        # Передача 1-2 сообщений
        messages = [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "What's the weather like today?"}
        ]

        response = await requests_gpt(messages)
        print("GPT response:", response)


    # Запуск асинхронной функции
    asyncio.run(main())
