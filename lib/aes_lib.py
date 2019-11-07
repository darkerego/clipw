import pyaes
import base64
from .clipw_conf import *


class HandleAes(object):
    """
    AES Encrypt/Decrypt Function
    """
    def __init__(self, key):
        self.key = key


    def encrypt_data(self, data):
        """
        ENCRYPTION
        AES CRT mode - 256 bit (32 byte) key
        :param data: data to encrypt
        :return: base64 wrapper AES encrypted data
        """
        key = self.key
        aes = pyaes.AESModeOfOperationCTR(key)
        ciphertext = aes.encrypt(data)
        encoded = base64.b64encode(ciphertext).decode('utf-8')
        if debug:
            print('Encrypted data:', encoded)
        # show the encrypted data
        return encoded

    def decrypt_data(self, data):
        """
        DECRYPTION
        AES CRT mode decryption requires a new instance be created
        :param data: base64 encoded ciphertext
        :return: plaintext
        """
        #  key = self.key
        aes = pyaes.AESModeOfOperationCTR(self.key)
        # decrypted data is always binary, need to decode to plaintext
        decoded = base64.b64decode(data)
        decrypted = aes.decrypt(decoded).decode('utf-8')
        if debug:
            print('Decrypted data:', decrypted)
        return decrypted
