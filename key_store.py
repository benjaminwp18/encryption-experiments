from abc import ABC, abstractmethod
from pathlib import Path

from file_io import FileHandler


class KeyStore(ABC):
    @abstractmethod
    def save_key(self, key: bytes, file_path: Path) -> None:
        pass

    @abstractmethod
    def load_key(self, file_path: Path) -> bytes:
        pass

    def save_keys(self, keys: list[bytes], file_paths: list[Path]) -> None:
        for key, file_path in zip(keys, file_paths):
            self.save_key(key, file_path)

    def load_keys(self, file_paths: list[Path]) -> list[bytes]:
        keys = []
        for file_path in file_paths:
            keys.append(self.load_key(file_path))
        return keys

class BytesKeyStore(KeyStore):
    def save_key(self, key: bytes, file_path: Path) -> None:
        FileHandler.save_file(file_path, key)

    def load_key(self, file_path: Path) -> bytes:
        return FileHandler.load_file(file_path)
