import hmac
import random
import string
from _hashlib import pbkdf2_hmac
from getpass import getpass
from os import urandom, mkdir
from typing import Tuple, Union, Optional
from lib.clipw_conf import debug, config_dir, config_file


class HashPass:
    """
    Wrapper Class for password hashing functions
    """
    def __init__(self):
        #  TODO: Remove this useless init function
        """
        Empty __init__ function
        """
        self.name = 'HashPass'

    def hash_new_password(self, password: str) -> Tuple[bytes, bytes]:

        """
        Hash the provided password with a randomly-generated salt and return the
        salt and hash to store in the database.
        :return salt, password hash
        """

        salt = urandom(16)
        pw_hash = pbkdf2_hmac('sha256', password.encode(), salt, 100000)
        return salt, pw_hash

    def check_pw_padding(self, pw: str) -> str:
        """
        Check that password length is AES compliant, add padding if not
        :param pw: password

        :return: password with buffering
        """

        pw_len = len(pw)
        if pw_len <= 8:
            while pw_len % 8 != 0:
                pw += '0'
                pw_len = (len(pw))
        if pw_len <= 16:
            while pw_len % 16 != 0:
                pw += '0'
                pw_len = (len(pw))
        if pw_len <= 32:
            while pw_len % 32 != 0:
                pw += '0'
                pw_len = (len(pw))

        return pw

    def is_correct_password(self, salt: bytes, pw_hash: bytes, password: str) -> bool:
        """
        Function to check pw to unlock db:
        Given a previously-stored salt and hash, and a password provided by a user
        trying to log in, check whether the password is correct.
        :param salt: salt
        :param pw_hash: hash
        :param password: check against this user supplied password

        :return: bool

        """

        return hmac.compare_digest(
            pw_hash,
            pbkdf2_hmac('sha256', password.encode(), salt, 100000)
        )

    def generate_hash(self, pw: str) -> Union[Tuple[str, str], bool]:
        """
        Generate a Hash and Salt from a password
        :param pw: password to hash

        :return: True or False
        """

        salt, pw_hash = self.hash_new_password(pw)
        salt = salt.hex()
        pw_hash = pw_hash.hex()
        if self.is_correct_password(bytes.fromhex(salt), bytes.fromhex(pw_hash), pw):
            if debug:
                print('Test Succeeded!')
                print("Salt: %s" % salt)
                print("Hash: %s" % pw_hash)
            return salt, pw_hash
        return False

    def store_master_password(self) -> bool:
        """
        Upon init, store users master key to disc

        :return: True on success
        """
        try:
            mkdir(config_dir)
        except FileExistsError as err:
            pass
        else:
            print('Created config directory %s' % config_dir)
        # hash a password
        while True:
            pw = getpass('Password: ')
            pw2 = getpass('Confirm: ')
            try:
                assert pw == pw2
            except AssertionError:
                print('Passwords do not match. Try again')
            else:
                # assert pw == pw2, 'Passwords do not match. Try again'
                pw_len = len(pw)
                if pw_len > 32 or pw_len < 8:
                    print('Password must be at least 8 and no more than 32 characters.')
                else:
                    s, p = self.generate_hash(pw)
                    hash_str = str(s + ":" + p)
                    with open(config_file, 'w+') as f:
                        f.write(hash_str)
                    return True

    # def get_master_password(self):
    def get_master_password(self) -> Union[bytes, None]:
        """
        Function to create an AES friendly Master Password
        to encrypt all the passwords in the database...
        Because they key needs to be either 8 or 16 characters,
        we will add padding until it if an appropriate length.

        :return: byte encoded password string
        """
        with open(config_file, 'r') as ff:
            master_hash = ff.read()
            _salt = master_hash.split(':')[0]
            _hash = master_hash.split(':')[1]
            master_pw = getpass("Master Password: ")
            if self.is_correct_password(bytes.fromhex(_salt), bytes.fromhex(_hash), master_pw):
                print('Successfully unlocked.')
                master_pw = self.check_pw_padding(master_pw)
                return master_pw.encode()
            else:
                print('Incorrect Password')
                exit(1)

    def store_password(self) -> str:
        """
        Function to get a password and confirm user enters it twice correctly.

        :return: password
        """
        while True:
            pw = getpass('Password: ')
            pw2 = getpass('Confirm: ')
            try:
                assert pw == pw2
            except AssertionError:
                print('Passwords do not match.')
            else:
                return pw

    def random_password(self, n: Optional[int] = 12) -> str:
        """
        Generate a random password of length n
        :param n: length of password to generate

        :return: password string
        """
        random_source = string.ascii_letters + string.digits + string.punctuation
        password = random.choice(string.ascii_lowercase)
        password += random.choice(string.ascii_uppercase)
        password += random.choice(string.digits)
        password += random.choice(string.punctuation)

        for i in range(n):
            password += random.choice(random_source)

        password_list = list(password)
        random.SystemRandom().shuffle(password_list)
        password = ''.join(password_list)[:n]
        return password
