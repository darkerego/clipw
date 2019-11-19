from typing import Union

import pyaes
import base64
from .clipw_conf import *


class HandleAes:
    """
    AES Encrypt/Decrypt Function
    """
    def __init__(self, key: object) -> None:
        """
        Init AES Lib with master key
        :param key:
        """
        self.key = key

    def remove_from_mem(self) -> None:
        """
        Clear key from memory on exit (for security)
        #  TODO: Is this necessary/sufficient/secure?

        :return: None
        """
        self.key = None

    def encrypt_data(self, data: str) -> Union[str, None]:
        """
        ENCRYPTION
        AES CRT mode - 256 bit (8, 16, or 32 byte) key
        :param data: data to encrypt

        :return: base64 wrapper AES encrypted data
        """
        aes = pyaes.AESModeOfOperationCTR(self.key)
        ciphertext = aes.encrypt(data)
        encoded = base64.b64encode(ciphertext).decode('utf-8')
        if debug:
            print('Encrypted data:', encoded)
        # show the encrypted data
        return encoded

    def decrypt_data(self, data: str) -> Union[str, None]:
        """
        DECRYPTION
        AES CRT mode decryption requires a new instance be created
        :param data: base64 encoded ciphertext

        :return: plaintext
        """
        aes = pyaes.AESModeOfOperationCTR(self.key)
        # decrypted data is always binary, need to decode to plaintext
        decoded = base64.b64decode(data)
        decrypted = aes.decrypt(decoded).decode('utf-8')
        if debug:
            print('Decrypted data:', decrypted)
        return decrypted
