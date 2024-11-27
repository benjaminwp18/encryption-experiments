from pathlib import Path
from PIL import Image, UnidentifiedImageError
import numpy as np
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding

from file_crypters.basic_crypters import CannotCrypt, FileCrypter
from file_io import FileHandler, FileSize


class VisualAESFileCrypter(FileCrypter):
    def __init__(self, key: bytes, max_file_size: FileSize) -> None:
        self.key = key[-16:]
        self.init_vector = key[:16]
        self.max_file_size = max_file_size

    def crypt(self, file_path: Path, encrypt: bool) -> None:
        if not FileHandler.is_legal_file(file_path, self.max_file_size):
            raise CannotCrypt()

        try:
            if encrypt:
                self._encrypt_visual_aes(file_path)
            else:
                self._decrypt_visual_aes(file_path)
        except (FileNotFoundError, UnidentifiedImageError) as _:
            raise CannotCrypt()

    def _encrypt_visual_aes(self, file_path: Path):
        img = Image.open(file_path)
        img = img.convert("RGB")
        img_array = np.array(img)

        print(len(self.key))

        cipher = Cipher(algorithms.AES(self.key), modes.CBC(self.init_vector), backend=default_backend())

        flat_data = img_array.flatten()

        # Pad data w/block_size that's a multiple of # img channels
        # That way we can keep the format when saving
        padder = padding.PKCS7(128 * img_array.shape[2]).padder()
        padded_data = padder.update(flat_data.tobytes()) + padder.finalize()

        encryptor = cipher.encryptor()
        encrypted_data = encryptor.update(padded_data) + encryptor.finalize()

        encrypted_array = np.frombuffer(encrypted_data, dtype=np.uint8)

        # Reshape to something close to square w/the right # channels
        encrypted_array = self._reshape_to_3d(encrypted_array, img_array.shape[2])

        # Prepend a metadata row that encodes the image dimensions in plaintext
        encrypted_array = self._prepend_metadata_row(encrypted_array, img_array.shape)

        encrypted_img = Image.fromarray(encrypted_array)
        encrypted_img.save(file_path)

    def _decrypt_visual_aes(self, file_path: Path):
        img = Image.open(file_path)
        img_array = np.array(img)

        # Read & pop the metadata row to get target img dimensions
        img_array, shape = self._pop_metadata_row(img_array)

        encrypted_data = img_array.flatten().tobytes()

        cipher = Cipher(algorithms.AES(self.key), modes.CBC(self.init_vector), backend=default_backend())

        decryptor = cipher.decryptor()
        decrypted_data = decryptor.update(encrypted_data) + decryptor.finalize()

        # Remove padding w/same block_size as encryption
        unpadder = padding.PKCS7(128 * shape[2]).unpadder()
        unpadded_data = unpadder.update(decrypted_data) + unpadder.finalize()

        img_array_decrypted = np.frombuffer(unpadded_data, dtype=np.uint8)
        img_array_decrypted = img_array_decrypted.reshape(shape)

        decrypted_img = Image.fromarray(img_array_decrypted)

        decrypted_img.save(str(file_path))

    @staticmethod
    def _prepend_metadata_row(arr: np.ndarray, img_shape: tuple[int, int, int]) -> np.ndarray:
        row = np.zeros((1, arr.shape[1], arr.shape[2]))

        dims_as_bytes = [list(dim.to_bytes(3, 'big')) for dim in img_shape]

        for d, dim in enumerate(dims_as_bytes):
            for b, byte in enumerate(dim):
                row[0][d][b] = byte

        return np.insert(arr, 0, row, axis=0)

    @staticmethod
    def _pop_metadata_row(arr: np.ndarray) -> tuple[np.ndarray, tuple[int, int, int]]:
        row = arr[0]
        shape = []
        for i in range(3):
            dim_as_bytes = bytes(row[i])
            shape.append(int.from_bytes(dim_as_bytes, 'big'))

        return (np.delete(arr, (0), axis=0), tuple(shape))

    @staticmethod
    def _reshape_to_3d(arr: np.ndarray, num_channels: int) -> np.ndarray:
        N = arr.size
        area = N // num_channels

        # Find the factors of the area that are as close as possible
        X, Y = None, None
        best_diff = float('inf')

        for i in range(1, int(np.sqrt(area)) + 1):
            if area % i == 0:
                x, y = i, area // i
                # Minimize the difference between X and Y to make them as square as possible
                if abs(x - y) < best_diff:
                    X, Y = x, y
                    best_diff = abs(x - y)

        reshaped_arr = arr.reshape(X, Y, num_channels)

        return reshaped_arr