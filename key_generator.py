from abc import ABC, abstractmethod
from cryptography.fernet import Fernet

class KeyGenerator(ABC):
    @abstractmethod
    def generate() -> bytes:
        pass

class FernetKeyGenerator(KeyGenerator):
    def generate() -> bytes:
        return Fernet.generate_key()