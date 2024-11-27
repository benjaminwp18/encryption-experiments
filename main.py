import argparse
from pathlib import Path

from file_crypter import InPlaceFileCrypter
from file_size import FileSize
from files_crypter import FilesCrypter
from key_generator import FernetKeyGenerator
from key_store import BytesKeyStore

KEY_PATH = Path('data') / 'keys' / 'key'
FILES_PATH = Path('data') / 'files'

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Simple File Encryptor Script')
    parser.add_argument('-e', '--encrypt', action='store_true',
                        help='Encrypt the target (DEFAULT, only -e or -d can be specified)')
    parser.add_argument('-d', '--decrypt', action='store_true',
                        help='Decrypt the target (only -e or -d can be specified)')

    args = parser.parse_args()

    encrypt = True
    if args.encrypt and args.decrypt:
        raise TypeError('Please specify only one of -e or -d.')
    else:
        # !args.decrypt instead of args.encrypt here for default of encrypt=True when nothing's specified
        encrypt = not args.decrypt

    key_store = BytesKeyStore()

    if encrypt:
        print('Generating key')
        key = FernetKeyGenerator.generate()
        key_store.save_key(key, KEY_PATH)
    else:
        print('Loading key')
        key = key_store.load_key(KEY_PATH)

    files_crypter = FilesCrypter([
        InPlaceFileCrypter(key, FileSize.from_mb(10))
    ])

    files_crypter.crypt([FILES_PATH], encrypt=encrypt)
