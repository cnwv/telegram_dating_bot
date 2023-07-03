import openai
from config import OpenAI

openai.api_key = OpenAI.api_key
print(type(OpenAI.api_key))


async def requests_gpt(text):
    print(f"text{text}")
    completion = openai.ChatCompletion.create(model="gpt-3.5-turbo",
                                              messages=text)
    response = completion.choices[0].message.content
    return response
