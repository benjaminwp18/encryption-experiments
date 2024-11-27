from abc import ABC, abstractmethod
from pathlib import Path

from file_io import FileHandler, FileSize
from cryptography.fernet import Fernet

class CannotCrypt(Exception):
    pass

class FileCrypter(ABC):
    def encrypt(self, file_path: Path) -> None:
        self.crypt(file_path, encrypt=True)

    def decrypt(self, file_path: Path) -> None:
        self.crypt(file_path, encrypt=False)

    @abstractmethod
    def crypt(self, file_path: Path, encrypt: bool) -> None:
        pass

class BytewiseFileCrypter(FileCrypter):
    def __init__(self, key: bytes, max_file_size: FileSize) -> None:
        self.fernet = Fernet(key)
        self.max_file_size = max_file_size

    def crypt(self, file_path: Path, encrypt: bool) -> None:
        if not FileHandler.is_legal_file(file_path, self.max_file_size):
            raise CannotCrypt()

        file_bytes = FileHandler.load_file(file_path)
        converted_bytes = self.fernet.encrypt(file_bytes) if encrypt else self.fernet.decrypt(file_bytes)
        FileHandler.save_file(file_path, converted_bytes)
