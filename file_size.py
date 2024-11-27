from __future__ import annotations

class FileSize():
    BYTES_IN_KB = 1024
    KB_IN_MB = 1024
    MB_IN_GB = 1024

    def __init__(self, size_in_bytes: int):
        self.size_in_bytes = size_in_bytes

    @staticmethod
    def from_bytes(size_in_bytes: int) -> FileSize:
        return FileSize(size_in_bytes)

    @staticmethod
    def from_kb(size_in_kb: int) -> FileSize:
        return FileSize.from_bytes(size_in_kb * FileSize.BYTES_IN_KB)

    @staticmethod
    def from_mb(size_in_mb: int) -> FileSize:
        return FileSize.from_kb(size_in_mb * FileSize.KB_IN_MB)

    @staticmethod
    def from_gb(size_in_gb: int) -> FileSize:
        return FileSize.from_mb(size_in_gb * FileSize.MB_IN_GB)

    def to_bytes(self) -> int:
        return self.size_in_bytes