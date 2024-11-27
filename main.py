import argparse
from pathlib import Path

from file_crypters.basic_crypters import BytewiseFileCrypter
from file_crypters.visual_aes import VisualAESFileCrypter
from file_io import FileSize
from files_crypter import FilesCrypter
from key_generator import FernetKeyGenerator
from key_store import BytesKeyStore

KEY_PATH = Path('data') / 'keys' / 'key'
FILES_PATH = Path('data') / 'files'

def get_bytes_key(encrypt: bool):
    key_store = BytesKeyStore()

    if encrypt:
        print('Generating key')
        key = FernetKeyGenerator.generate()
        key_store.save_key(key, KEY_PATH)
    else:
        print('Loading key')
        key = key_store.load_key(KEY_PATH)

    return key

def basic_crypter(encrypt: bool):
    key = get_bytes_key(encrypt)

    files_crypter = FilesCrypter([
        BytewiseFileCrypter(key, FileSize.from_mb(10))
    ])

    files_crypter.crypt([FILES_PATH], encrypt=encrypt)

def visual_aes_crypter(encrypt: bool):
    key = get_bytes_key(encrypt)

    files_crypter = FilesCrypter([
        VisualAESFileCrypter(key, FileSize.from_mb(10))
    ])

    files_crypter.crypt([FILES_PATH], encrypt=encrypt)

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

    visual_aes_crypter(encrypt)
