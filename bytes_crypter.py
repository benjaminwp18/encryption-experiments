from cryptography.fernet import Fernet

class BytesCrypter():
    def __init__(self, key) -> None:
        self.fernet = Fernet(key)

    def encrypt(self, plain_text: bytes) -> bytes:
        return self.fernet.encrypt(plain_text)

    def decrypt(self, cipher_text: bytes) -> bytes:
        return self.fernet.decrypt(cipher_text)

    def crypt(self, text: bytes, encrypt: bool) -> bytes:
        if encrypt:
            return self.encrypt(text)
        else:
            return self.decrypt(text)