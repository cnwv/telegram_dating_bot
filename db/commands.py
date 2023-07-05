from db.engine import Database
from db import schema
from sqlalchemy import update
from config import OpenAI


class DbCommands(Database):
    def __init__(self):
        Database.__init__(self)

    def create_user(self, id, nickname):
        session = self.maker()
        is_user = session.query(schema.Users).filter_by(id=id).first()
        if not is_user:
            user = schema.Users(id=id, nickname=nickname, premium=False)
            session.add(user)
            session.commit()
            session.close()

    def delete_message(self, user_id):
        session = self.maker()
        session.query(schema.Messages).filter(schema.Messages.user_id == user_id).delete(synchronize_session=False)
        session.commit()
        session.close()

    def add_message(self, id, text, role):
        messages = [
            {"role": "assistant", "content": f"{OpenAI.promt}"}
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
                update_messages = update(schema.Messages).where(schema.Messages.user_id == id).values \
                    ({schema.Messages.message: existing_message.message + [{'role': role, 'content': text}]})
                session.execute(update_messages)
                session.commit()
                dialog = session.query(schema.Messages).filter_by(user_id=id).first()
                session.close()
                return dialog.message


db = DbCommands()
