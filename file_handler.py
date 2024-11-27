from pathlib import Path

from file_size import FileSize


class FileHandler():
    @staticmethod
    def load_file(file_path: Path) -> bytes:
        with open(str(file_path), 'rb') as file:
            return file.read()

    @staticmethod
    def save_file(file_path: Path, file_bytes: bytes) -> None:
        with open(str(file_path), 'wb') as file:
            file.write(file_bytes)

    @staticmethod
    def is_legal_file(file_path: Path, max_file_size: FileSize = None):
        return (
            file_path.is_file() and not file_path.is_symlink()
            and (
                max_file_size is None or
                file_path.stat().st_size <= max_file_size.to_bytes()
            )
        )