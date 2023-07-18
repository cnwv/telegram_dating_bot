import openai
from config import OpenAI
import asyncio
from db.commands import db

apy_key_list = eval(OpenAI.api_key)

message_prefix = ['Знакомство вживую. Подробности:',
                  'Знакомство по сети. Подробности:']


async def requests_gpt(text, id):
    api_key = apy_key_list.pop(0)
    openai.api_key = api_key
    apy_key_list.append(api_key)
    state = db.get_message_state(id)
    if state:
        # true - онлайн знакомство
        text = f"{message_prefix[1]} {text}"
        db.set_message_state_to_none(id)
    elif state is False:
        # false - офлайн знакомство
        text = f"{message_prefix[0]} {text}"
        db.set_message_state_to_none(id)
    else:
        # none - без условия
        pass
    dialog = db.add_message(id, text, "user")
    print(dialog)
    print('GPT request')
    completion = openai.ChatCompletion.create(model="gpt-3.5-turbo",
                                              messages=dialog, max_tokens=2000)
    response = completion.choices[0].message.content
    db.add_message(id, response, 'assistant')
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
