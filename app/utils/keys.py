from app import app
import os
from Crypto.PublicKey import RSA

# This file will be responsible for storing retrieving public and private keys

def generate_keys(username):
    if get_public_key(username):
        return 0
    keys = RSA.generate(2048)
    private_key = keys.export_key()
    public_key = keys.publickey().export_key()
    path = os.path.join(app.config['KEYS_DIR'],username+'_private.pem')
    with open(path, 'wb') as file:
        file.write(private_key)
    store_public_key(username, public_key.decode())
    return 1

def get_public_key(username):
    path = os.path.join(app.config['KEYS_DIR'],username+'_public.pem')
    try:
        with open(path) as file:
            return file.read()
    except FileNotFoundError:
        return None

def store_public_key(username, key):
    path = os.path.join(app.config['KEYS_DIR'],username+'_public.pem')
    with open(path, 'w') as file:
        file.write(key)

def check_private_key(username):
    path = os.path.join(app.config['KEYS_DIR'],username+'_private.pem')
    return os.path.exists(path)
