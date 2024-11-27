from pathlib import Path
from PIL import Image, UnidentifiedImageError
import random

from file_crypters.basic_crypters import CannotCrypt, FileCrypter
from file_io import FileHandler, FileSize


class PixelShuffleFileCrypter(FileCrypter):
    def __init__(self, key: bytes, max_file_size: FileSize) -> None:
        self.key = key
        self.max_file_size = max_file_size

    def crypt(self, file_path: Path, encrypt: bool) -> None:
        if not FileHandler.is_legal_file(file_path, self.max_file_size):
            raise CannotCrypt()

        try:
            image = Image.open(file_path)
        except (FileNotFoundError, UnidentifiedImageError) as _:
            raise CannotCrypt()

        # list of e.g. (r,g,b) pixels
        pixels = list(image.getdata())
        randomizer = random.Random(self.key)

        indices = list(range(len(pixels)))
        randomizer.shuffle(indices)

        if encrypt:
            # Shuffle pixels
            converted_pixels = [pixels[i] for i in indices]
        else:
            converted_pixels = [None] * len(pixels)

            # Unshuffle pixels
            for original_index, shuffled_index in enumerate(indices):
                converted_pixels[shuffled_index] = pixels[original_index]

        converted_image = Image.new(image.mode, image.size)
        converted_image.putdata(converted_pixels)
        converted_image.save(file_path)