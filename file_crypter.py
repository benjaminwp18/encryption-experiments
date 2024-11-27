from abc import ABC, abstractmethod
from pathlib import Path

from bytes_crypter import BytesCrypter
from file_handler import FileHandler
from file_size import FileSize

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

class InPlaceFileCrypter(FileCrypter):
    def __init__(self, key: bytes, max_file_size: FileSize) -> None:
        self.bytes_crypter = BytesCrypter(key)
        self.max_file_size = max_file_size

    def crypt(self, file_path: Path, encrypt: bool) -> None:
        if FileHandler.is_legal_file(file_path, self.max_file_size):
            file_bytes = FileHandler.load_file(file_path)
            converted_bytes = self.bytes_crypter.crypt(file_bytes, encrypt)
            FileHandler.save_file(file_path, converted_bytes)
        else:
            raise CannotCrypt()