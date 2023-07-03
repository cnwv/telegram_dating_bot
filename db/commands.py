from db.engine import Database
from db import schema
import asyncio
import json
from sqlalchemy import update

class DbCommands(Database):
    def __init__(self):
        Database.__init__(self)

    async def test(self):
        text = [
            {"role": "user", "content": "Hello"},
            {"role": "assistant", "content": "Hi, how can I assist you today?"},
            {"role": "user", "content": "I have a question about your products."},
            {"role": "assistant", "content": "Sure, I'd be happy to help. What would you like to know?"},
            {"role": "user", "content": "Can you tell me about the pricing options?"},
            {"role": "assistant",
             "content": "Certainly! We have different pricing plans based on your needs. Could you please provide more details about your requirements?"},
            {"role": "user",
             "content": "I'm looking for a plan that includes unlimited storage and advanced analytics."},
            {"role": "assistant",
             "content": "We have a premium plan that offers unlimited storage, advanced analytics, and additional features. It costs $99 per month."},
            {"role": "user", "content": "That sounds great! How can I sign up for the premium plan?"},
            {"role": "assistant",
             "content": "To sign up for the premium plan, you can visit our website and follow the instructions on the pricing page. Let me know if you need any further assistance."},
        ]
        session = self.maker()
        employee = schema.Messages(id=360765221, message=text)
        session.add(employee)
        session.commit()
        session.close()

    def create_user(self, id, nickname):
        session = self.maker()
        is_user = session.query(schema.Users).filter_by(id=id).first()
        if not is_user:
            user = schema.Users(id=id, nickname=nickname, premium=False)
            session.add(user)
            session.commit()
            session.close()

    def add_message(self, id, text, role):
        messages = [
            {"role": "assistant", "content": "Добро пожаловать в помощника по знакомствам!"}
        ]
        session = self.maker()
        user = session.query(schema.Users).filter_by(id=id).first()
        if user:
            existing_message = session.query(schema.Messages).filter_by(user_id=id).first()
            if not existing_message:
                messages.append({"role": role, "content": text})
                message = schema.Messages(user_id=user.id, message=messages)
                session.add(message)
                session.commit()
                session.close()
                return messages
            else:
                print('вторая')
                update_messages = update(schema.Messages).where(schema.Messages.user_id == id).values\
                    ({schema.Messages.message: existing_message.message + [{'role': role, 'content': text}]})
                session.execute(update_messages)
                session.commit()
                dialog = session.query(schema.Messages).filter_by(user_id=id).first()
                session.close()
                return dialog.message







db = DbCommands()

