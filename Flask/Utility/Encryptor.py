from cryptography.fernet import Fernet
from cryptography.fernet import InvalidToken
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
        print (message)
        print (message.encode("ascii"))
        decrypted_message = self.cipher.decrypt(message.encode("ascii"))
        token = json.loads((decrypted_message).decode())
        return token
    def getKey(self):
        return self.key