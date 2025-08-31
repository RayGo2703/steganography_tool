from cryptography.fernet import Fernet
import base64
import hashlib

def _get_key(password):
    return base64.urlsafe_b64encode(hashlib.sha256(password.encode()).digest())

def encrypt_message(message, password):
    key = _get_key(password)
    f = Fernet(key)
    return f.encrypt(message.encode()).decode()

def decrypt_message(ciphertext, password):
    key = _get_key(password)
    f = Fernet(key)
    return f.decrypt(ciphertext.encode()).decode()