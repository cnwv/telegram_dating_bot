from os import getenv
from dotenv import load_dotenv

load_dotenv()


class DB:
    host = getenv('HOST')
    user_db = getenv('USER_DB')
    password = getenv('PASSWORD')
    db_name = getenv('DB_NAME')
    port = getenv('PORT')
    URL = f"postgresql://{user_db}:{password}@{host}:{port}/{db_name}"


class Telegram:
    debug = int(getenv('DEBUG'))
    api_key = getenv('BOT_TOKEN')
    payment_key = getenv('PAYMENTS_TOKEN')
    start_text = getenv('START_TEXT')
    expire_text = getenv('EXPIRE_TEXT')


class OpenAI:
    api_key = getenv('OPEN_AI_TOKEN')
    promt = getenv('PROMT_GPT')


class Ngrok:
    url = getenv('NGROK_URL')
