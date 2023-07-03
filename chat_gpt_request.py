import openai
from config import OpenAI

openai.api_key = OpenAI.api_key
print(type(OpenAI.api_key))

def requests_gpt(text):
    completion = openai.ChatCompletion.create(model="gpt-3.5-turbo",
                                              messages=[{"role": "user", "content": "Hello world"}])
    response = completion.choices[0].message.content
    print(response)
requests_gpt('dsds')