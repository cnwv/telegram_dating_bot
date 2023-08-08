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
    start_text = getenv('START_TEXT')
    expire_text = getenv('EXPIRE_TEXT')


class OpenAI:
    api_key = getenv('OPEN_AI_TOKEN')
    promt = getenv('PROMT_GPT')


class Web:
    ngrok_url = getenv('NGROK_URL')
    main_url = getenv('MAIN_URL')


class Robokassa:
    password_1 = getenv('PASSWORD_1')
    password_2 = getenv('PASSWORD_2')
    test_password_1 = getenv('TEST_PASSWORD_1')
    test_password_2 = getenv('TEST_PASSWORD_2')
