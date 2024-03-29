import time
import socketio
from app import app, cache, client_conn
from app.models import add_message
from app.utils.encryption import encrypt, decrypt

server_conn = socketio.Client()
TOKEN = cache.get('token')

@client_conn.on('connect')
def on_connect():
    print('Client connected')

@server_conn.on('message')
def on_message(data):
    # TODO: Store the message in the database
    # and pass it to the client
    print("From Server", data)
    data['message'] = decrypt(data['message'], cache.get('username'))
    with app.app_context():
        add_message(data['from'], data['message'], False, data['timestamp'])
    client_conn.emit('message', data)

@client_conn.on('message')
def on_message(data):
    # TODO: Store the message in the database
    # and pass it to the server
    print(data)
    with app.app_context():
        add_message(data['username'], data['message'], True, int(time.time()))
    data['message'] = encrypt(data['message'], data['username'])
    server_conn.emit( 'message',{
        'token' : TOKEN,
        'to' : data['username'],
        'message' : data['message']
    })

def connect_to_server():
    global TOKEN, server_conn
    if server_conn.connected:
        return
    TOKEN = cache.get('token')    
    server_conn.connect(app.config["SERVER_API"], auth={'token': TOKEN})