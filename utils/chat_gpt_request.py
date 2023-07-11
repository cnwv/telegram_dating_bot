import openai
from config import OpenAI
import asyncio
openai.api_key = OpenAI.api_key


async def requests_gpt(text):
    print(text)
    print('GPT request')
    completion = openai.ChatCompletion.create(model="gpt-3.5-turbo",
                                              messages=text)
    response = completion.choices[0].message.content
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