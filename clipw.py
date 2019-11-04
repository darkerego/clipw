#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CliPassWord Manager - A Very Simple Python3 Powered Command Line Password Manager
Author: Darkerego ~ November, 2019 <xelectron@protonmail.com>
"""
from typing import Tuple
from os import urandom, mkdir, getenv
from hashlib import pbkdf2_hmac
import hmac
from getpass import getpass
import random
import string
import argparse
import sqlite3
import pyaes
import base64
# Runtime global variables
debug = False
config_dir = getenv('HOME') + '/.clipw'
config_file = config_dir + '/clipw.conf'
database_file = config_dir + '/clipw.db'


def encrypt_data(data, key):
    """
    ENCRYPTION
    AES CRT mode - 256 bit (32 byte) key
    :param data: data to encrypt
    :return: base64 wrapper AES encrypted data
    """
    aes = pyaes.AESModeOfOperationCTR(key)
    ciphertext = aes.encrypt(data)
    encoded = base64.b64encode(ciphertext).decode('utf-8')
    if debug:
        print('Encrypted data:', encoded)
    # show the encrypted data
    return encoded


def decrypt_data(data, key):
    """
    DECRYPTION
    AES CRT mode decryption requires a new instance be created
    :param data: base64 encoded ciphertext
    :return: plaintext
    """
    aes = pyaes.AESModeOfOperationCTR(key)
    # decrypted data is always binary, need to decode to plaintext
    decoded = base64.b64decode(data)
    decrypted = aes.decrypt(decoded).decode('utf-8')
    if debug:
        print('Decrypted data:', decrypted)
    return decrypted


def init_database():

    global sqliteConnection
    try:
        sqliteConnection = sqlite3.connect(database_file)
        sqlite_create_table_query = '''CREATE TABLE Password_Store (
                                    id INTEGER PRIMARY KEY,
                                    desc text NOT NULL,
                                    pass_hash text NOT NULL);'''

        cursor = sqliteConnection.cursor()
        print("Successfully Connected to SQLite")
        cursor.execute(sqlite_create_table_query)
        sqliteConnection.commit()
        print("SQLite table created")

        cursor.close()

    except sqlite3.Error as error:
        print("Error while creating a sqlite table", error)
    finally:
        if (sqliteConnection):
            sqliteConnection.close()
            print("sqlite connection is closed")


def append_database(new_passwd, pw_description):
    """
    TODO: SQL insert into database
    :param new_passwd:
    :param pw_description:
    :return:
    """

    global sqliteConnection
    try:
        sqliteConnection = sqlite3.connect(database_file)
        cursor = sqliteConnection.cursor()
        if debug:
            print("Connected to SQLite")
        dataCopy = cursor.execute("select count(*) from Password_Store")
        values = dataCopy.fetchone()
        id = int(values[0])
        sqlite_insert_with_param = """INSERT INTO 'Password_Store'
                          ('id', 'desc', 'pass_hash') 
                          VALUES (?, ?, ?);"""

        data_tuple = (id, str(pw_description), str(new_passwd))
        cursor.execute(sqlite_insert_with_param, data_tuple)
        sqliteConnection.commit()
        if debug:
            print("Python Variables inserted successfully into SqliteDb_developers table")

        cursor.close()

    except sqlite3.Error as error:
        print("Failed to insert Python variable into sqlite table", error)
    else:
        print('Stored password ok.')
    finally:
        if sqliteConnection:
            sqliteConnection.close()
            if debug:
                print("The SQLite connection is closed")


def open_database():
    """
    TODO: Open database, show entries, prompt user for entry key, show password
    :param master_pw:
    :return:
    """
    global sqlite_connection
    try:
        sqlite_connection = sqlite3.connect(database_file)
        cursor = sqlite_connection.cursor()
        if debug:
            print("Connected to SQLite")

        sqlite_select_query = """SELECT * from Password_Store"""
        cursor.execute(sqlite_select_query)
        records = cursor.fetchall()
        if debug:
            print("Total rows are:  ", len(records))

        id_desc = []
        for row in records:
            _id = int(row[0])
            _desc = str(row[1])
            id_desc.append([_id, _desc])
        cursor.close()
        return id_desc
    except sqlite3.Error as error:
        print("Failed to read data from sqlite table", error)
    finally:
        if sqlite_connection:
            sqlite_connection.close()
            if debug:
                print("The SQLite connection is closed")


def select_from_db(id):
    """
    Grab a certain password from the database
    :param id: primary key of password to get
    :return: aes encrypted password
    """
    global sqliteConnection
    try:
        sqliteConnection = sqlite3.connect(database_file)
        cursor = sqliteConnection.cursor()
        if debug:
            print("Connected to SQLite")

        sql_select_query = """select * from Password_Store where id = ?"""
        cursor.execute(sql_select_query, (id,))
        record = cursor.fetchone()
        print("Retrieving ID ", id)
        cursor.close()
        return record

    except sqlite3.Error as error:
        print("Failed to read data from sqlite table", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()
            if debug:
                print("The SQLite connection is closed")


def hash_new_password(password: str) -> Tuple[bytes, bytes]:
    """
    Hash the provided password with a randomly-generated salt and return the
    salt and hash to store in the database.
    """
    salt = urandom(16)
    pw_hash = pbkdf2_hmac('sha256', password.encode(), salt, 100000)
    return salt, pw_hash


def check_pw_padding(pw):
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
        return pw
    if pw_len <= 16:
        while pw_len % 16 != 0:
            pw += '0'
            pw_len = (len(pw))
        return pw
    if pw_len <= 32:
        while pw_len % 32 != 0:
            pw += '0'
            pw_len = (len(pw))


def is_correct_password(salt: bytes, pw_hash: bytes, password: str) -> bool:
    """
    Given a previously-stored salt and hash, and a password provided by a user
    trying to log in, check whether the password is correct.
    """

    return hmac.compare_digest(
        pw_hash,
        pbkdf2_hmac('sha256', password.encode(), salt, 100000)
    )


def generate_hash(pw):
    """
    Generate a Hash and Salt from a password
    :param pw: password to hash
    :return: salt and hash
    """
    salt, pw_hash = hash_new_password(pw)
    salt = salt.hex()
    pw_hash = pw_hash.hex()
    if is_correct_password(bytes.fromhex(salt), bytes.fromhex(pw_hash), pw):
        if debug:
            print('Test Succeeded!')
            print("Salt: %s" % salt)
            print("Hash: %s" % pw_hash)
        return salt, pw_hash
    else:
        return False


def store_master_password():
    """
    Upon init, store users master key to disc
    :return: --
    """
    global pw
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
        if pw == pw2:
            pw_len = len(pw)
            if pw_len > 32 or pw_len < 8:
                print('Password must be at least 8 and no more than 32 characters.')
                exit(1)
            else:
                s, p = generate_hash(pw)
                hash_str = str(s + ":" + p)
                with open(config_file, 'w+') as f:
                    f.write(hash_str)
                return True

        else:
            print('Passwords do not match. Try again')


def get_master_password():
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
        if is_correct_password(bytes.fromhex(_salt), bytes.fromhex(_hash), master_pw):
            print('Success!')
            master_pw = check_pw_padding(master_pw)
            return master_pw.encode()
        else:
            print('Incorrect Password')
            exit(1)


def store_password(master_key):
    """
    Function to encrypt a password before inserting into database
    :param master_key:
    :return:
    """
    while True:
        pw = getpass('Password: ')
        pw2 = getpass('Confirm: ')
        if pw == pw2:
            encrypted_pw = encrypt_data(pw, master_key)
            return encrypted_pw


def random_password(n: int = 12) -> object:
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
    password = ''.join(password_list)
    return password


def get_args():
    """
    Argument parser
    :return: args
    """
    parser = argparse.ArgumentParser(description='Python Cli Password Manager')
    parser.add_argument('-i,' '--init_database', dest='init_db', action='store_true', help='Re|Init Database')
    parser.add_argument('-s', '--store', dest='store', action='store_true', help='Enter and store a new password in'
                                                                                 ' the database')
    parser.add_argument('-r', '--random', dest='gen_random', help='Generate and store a random password of n length',
                        type=int, default=0, nargs=1)
    parser.add_argument('-o', '--open', dest='open', help='Open the password database', action='store_true')
    return parser.parse_args()


def main():
    """
    Program main logic
    :return:
    """
    args = get_args()
    if args.init_db:
        store_master_password()
        init_database()
    if args.store:
        master_pw = get_master_password()
        pw_description = input('Description: ')
        new_passwd = store_password(master_pw)
        append_database(new_passwd, pw_description)
        exit(0)

    if args.gen_random:
        master_pw = get_master_password()
        pw_description = input('Description: ')
        pw_len = args.gen_random
        new_pw = random_password(pw_len[0])
        encrypted_pw = encrypt_data(new_pw, master_pw)
        append_database(encrypted_pw, pw_description)
        print('Password:', new_pw)
        exit(0)
    if args.open:
        master_pw = get_master_password()
        id_desc = open_database()
        for i in id_desc:
            print('ID: ', i[0], "Description", i[1])
        get = input('Enter ID of password to decrypt: ')
        try:
            get = int(get)
        except ValueError:
            print('Enter an integer!')
        else:
            if debug:
                print('Retrieving: ', get)

            ret = select_from_db(id=get)
            # print("Id: ", ret[0])
            print("Description:", ret[1])
            hashed = ret[2]
            decrypted = decrypt_data(hashed, master_pw)
            print('Password:', decrypted)


if __name__ == "__main__":
    main()

