from abc import ABC, abstractmethod
from cryptography.fernet import Fernet

class KeyGenerator(ABC):
    @staticmethod
    @abstractmethod
    def generate() -> bytes:
        pass

class FernetKeyGenerator(KeyGenerator):
    @staticmethod
    def generate() -> bytes:
        return Fernet.generate_key()