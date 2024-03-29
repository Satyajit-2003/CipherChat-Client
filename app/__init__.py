from flask import Flask
from flask_socketio import SocketIO
from flask_sqlalchemy import SQLAlchemy
from flask_caching import Cache
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)
cache = Cache(app)
client_conn = SocketIO(app, cors_allowed_origins="*")

from app import routes
from app import socket
