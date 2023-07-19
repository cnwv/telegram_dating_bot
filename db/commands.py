from db.engine import Database
from db import schema
from sqlalchemy import update
from config import OpenAI
import logging


class DbCommands(Database):
    def __init__(self):
        Database.__init__(self)

    def create_user(self, id, nickname):
        session = self.maker()
        is_user = session.query(schema.Users).filter_by(id=id).first()
        if not is_user:
            print('попали в юзерс')
            user = schema.Users(id=id, nickname=nickname, premium=False)
            session.add(user)
            session.commit()
            session.close()
            session = self.maker()
            messages = schema.Messages(user_id=id, message=None, is_online=None)
            session.add(messages)
            session.commit()
            session.close()

    def delete_message(self, user_id):
        session = self.maker()
        session.query(schema.Messages).filter(schema.Messages.user_id == user_id).update({"message": None})
        session.commit()
        session.close()

    def add_message(self, id, text, role, username=None):
        messages = [
            {"role": "assistant", "content": f"{OpenAI.promt}"}
        ]
        session = self.maker()
        user = session.query(schema.Users).filter_by(id=id).first()
        if user:
            existing_message = session.query(schema.Messages.message).filter_by(user_id=id).first()
            print(type(existing_message))
            print(existing_message)
            if existing_message[0] is None:
                print('null')
                messages.append({"role": role, "content": text})
                # message = schema.Messages(user_id=user.id, message=messages)
                update_message = update(schema.Messages).where(schema.Messages.user_id == id).values(message=messages)
                session.execute(update_message)
                session.commit()
                session.close()
                return messages
            else:
                print('not null')
                update_messages = update(schema.Messages).where(schema.Messages.user_id == id).values \
                    ({schema.Messages.message: existing_message.message + [{'role': role, 'content': text}]})
                session.execute(update_messages)
                session.commit()
                dialog = session.query(schema.Messages).filter_by(user_id=id).first()
                session.close()
                return dialog.message
        else:
            self.create_user(id, username)
            messages.append({"role": role, "content": text})
            update_message = update(schema.Messages).where(schema.Messages.user_id == id).values(message=messages)
            session.execute(update_message)
            session.commit()
            session.close()
            return messages

    def add_type_of_relationship(self, id, is_online):
        print(is_online)
        session = self.maker()
        user = session.query(schema.Users).filter_by(id=id).first()
        if user:
            message = session.query(schema.Messages).filter_by(user_id=id).first()
            if message:
                update_status = update(schema.Messages).where(schema.Messages.user_id == id).values(is_online=is_online)
                session.execute(update_status)
                session.commit()
                session.close()
            else:
                pass
        else:
            pass

    def empty_message(self, id):
        session = self.maker()
        message = session.query(schema.Messages).filter_by(user_id=id).first()
        if message is None:
            messages = schema.Messages(user_id=id, message=None, is_online=None)
            session.add(messages)
            session.commit()
        session.close()

    def set_message_state_to_none(self, id):
        session = self.maker()
        update_status = update(schema.Messages).where(schema.Messages.user_id == id).values(is_online=None)
        session.execute(update_status)
        session.commit()
        session.close()

    def get_message_state(self, id):
        session = self.maker()
        message = session.query(schema.Messages).filter_by(user_id=id).first()
        if message:
            return message.is_online
        return None


db = DbCommands()
if __name__ == '__main__':
    db.create_user('1', 'loh')

