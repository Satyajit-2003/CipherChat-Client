from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP, AES
from Crypto.Util.Padding import pad, unpad
from app import app
import os

def encrypt(message, username):
    path = os.path.join(app.config['KEYS_DIR'], username + '_public.pem')
    public_key = RSA.import_key(open(path).read())
    cipher_rsa = PKCS1_OAEP.new(public_key)
    print("Encrypting with: ", path)
    encrypted_message = cipher_rsa.encrypt(message.encode())

    return encrypted_message.decode('ISO-8859-1')

def decrypt(encrypted_message, username):
    encrypted_message = encrypted_message.encode('ISO-8859-1')
    path = os.path.join(app.config['KEYS_DIR'], username + '_private.pem')
    private_key = RSA.import_key(open(path).read())
    cipher_rsa = PKCS1_OAEP.new(private_key)
    print("Decrypting with: ", path)
    message = cipher_rsa.decrypt(encrypted_message)

    return message.decode()

def encrypt_db(message):
    cipher = AES.new(app.config['AES_KEY'], AES.MODE_CBC, app.config['AES_IV'])
    message = message.encode()
    ct_bytes = cipher.encrypt(pad(message, AES.block_size))
    return ct_bytes.decode('ISO-8859-1')

def decrypt_db(ct_bytes):
    ct_bytes = ct_bytes.encode('ISO-8859-1')
    cipher = AES.new(app.config['AES_KEY'], AES.MODE_CBC, app.config['AES_IV'])
    pt = unpad(cipher.decrypt(ct_bytes), AES.block_size)
    return pt.decode()