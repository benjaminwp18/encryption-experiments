from pathlib import Path
import os
import warnings

from file_crypter import FileCrypter, CannotCrypt

class FilesCrypter():
    def __init__(self, file_crypters: list[FileCrypter]):
        self.file_crypters = file_crypters

    @staticmethod
    def load_files(paths: list[Path]) -> list[Path]:
        file_paths = []
        for file_path in paths:
            path_str = str(file_path)
            if file_path.is_dir():
                print(f'Enumerating files in "{path_str}"')
                for current_dir, _child_dirs, child_files in os.walk(path_str):
                    file_paths += [Path(os.path.join(current_dir, file)) for file in child_files]
            else:
                file_paths.append(file_path)

        return file_paths

    def encrypt(self, paths: list[Path]):
        self.crypt(paths, encrypt=True)

    def decrypt(self, paths: list[Path]):
        self.crypt(paths, encrypt=False)

    def crypt(self, paths: list[Path], encrypt: bool) -> None:
        print('Encrypting' if encrypt else 'Decrypting')

        file_paths = FilesCrypter.load_files(paths)
        for file_path in file_paths:
            for i, crypter in enumerate(self.file_crypters):
                try:
                    crypter.crypt(file_path, encrypt=encrypt)
                    break
                except CannotCrypt as e:
                    print(f'{str(file_path)} falls through crypter {i}')

                    if i == len(self.file_crypters) - 1:
                        warnings.warn(f'{str(file_path)} not processed by any crypters, skipping')
