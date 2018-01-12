from cryptography.fernet import Fernet
import base64
from flaskapp import app
import json




class Encryptor:

    @classmethod
    def __init__(self):
        self.key = app.config['COOKIE_KEY']
        self.cipher = Fernet(self.key)
    def encryptMessage(self, message):
        token = self.cipher.encrypt(bytes(message, encoding="ascii"))
        return token.decode()
    def decryptMessage(self, message):
        decrypted_message = self.cipher.decrypt(bytes(message, encoding="ascii"))
        token = json.loads((decrypted_message).decode())
        return token
    def getKey(self):
        return self.key