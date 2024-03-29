from app import app, db
import time
from app.utils.encryption import encrypt_db, decrypt_db

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    other_user = db.Column(db.String(100), nullable=False)
    message = db.Column(db.String(100000), nullable=False)
    send = db.Column(db.Boolean, nullable=False)  # True if the message was sent, False if it was received
    timestamp = db.Column(db.Integer, nullable=False)

def get_messages(username):
    messages = Message.query.filter_by(other_user=username).all()
    print("Is this working?")
    for message in messages:
        message.message = decrypt_db(message.message)
    return messages

def add_message(username, message, send, timestamp = int(time.time())):
    message = encrypt_db(message)
    new_message = Message(other_user=username, message=message, send=bool(send), timestamp=timestamp)
    db.session.add(new_message)
    db.session.commit()

with app.app_context():
    db.create_all()
