import os

class Config:
    SECRET_KEY = '5791628bb0b13ce0c676dfde280ba245'
    BASEDIR = os.path.abspath(os.path.dirname(__file__))
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASEDIR,'app','db','database.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SERVER_API = "http://13.235.104.168:5000"
    KEYS_DIR = os.path.join(BASEDIR,'app','keys')
    CACHE_TYPE = 'simple'
    AES_KEY = b'mysecretpassword'
    AES_IV = b'16bitIVforAESAES'