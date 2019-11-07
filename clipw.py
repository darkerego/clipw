#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CliPassWord Manager - A Very Simple Python3 Powered Command Line Password Manager
Author: Darkerego ~ November, 2019 <xelectron@protonmail.com>
"""
import argparse
from lib import aes_lib
from lib.clipw_conf import *
from lib import sql_functions
import lib.passlib
# Runtime global variables


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
    parser.add_argument('-e', '--edit', dest='edit', help='Edit an entry.', action='store_true')
    parser.add_argument('-d', '--delete', dest='delete', help='Delete an entry', action='store_true')
    return parser.parse_args()


def main():
    """
    Program main logic
    :return:
    """

    args = get_args()
    sql = sql_functions.Sql()
    if args.init_db:
        Hash_pass.store_master_password()
        sql.init_database()
        sql.close()
    if args.store:
        pw_description = input('Description: ')

        new_passwd = Hash_pass.store_password()
        encrypted_pw = aes.encrypt_data(new_passwd)
        sql.append_database(encrypted_pw, pw_description)
        sql.close()
        exit(0)

    if args.gen_random:
        pw_description = input('Description: ')
        pw_len = args.gen_random
        new_pw = Hash_pass.random_password(pw_len[0])
        encrypted_pw = aes.encrypt_data(new_pw)
        sql.append_database(encrypted_pw, pw_description)
        print('Password:', new_pw)
        exit(0)
    if args.open:
        id_desc = sql.open_database()
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
            #  sql = sql_functions.Sql()
            ret = sql.select_from_db(id=get)
            print("Id: ", ret[0])
            print("Description:", ret[1])
            hashed = ret[2]
            decrypted = aes.decrypt_data(hashed)
            print('Password:', decrypted)
            sql.close()

    if args.edit:
        """ This is the broken update logic, see edit_database() function"""
        id_desc = sql.open_database()
        for i in id_desc:
            print('ID: ', i[0], "Description", i[1])
        get = input('Enter ID of entry to edit: ')
        try:
            get = int(get)
        except ValueError:
            print('Enter an integer!')
        else:
            #  sql = sql_functions.Sql()
            ret = sql.select_from_db(id=get)
            #  sql = sql_functions.Sql()
            print('Fields: ')
            print('ID:', ret[0])
            print('[1] Description', ret[1])
            show_passwd = input('Show password (y/n)? : ')
            if show_passwd == 'y':
                hashed = ret[2]
                decrypted = aes.decrypt_data(hashed)
                print('[2] Password:', decrypted)
            else:
                print('[2] Password: x-x-x-x-x')

            print('Enter field to edit. Enter 1 for description, 2 for password ...')

            while True:
                try:
                    edit_field = int(input('Enter field: '))
                except TypeError:
                    print('Enter either 1 (description) or 2 (password)')
                else:
                    break
            if edit_field == 1:
                new_description = input('Description: ')
                try:
                    sql.edit_database(id=get, field='desc', data=new_description)
                except Exception as err:
                    print('Error editing entry:', err)
                finally:
                    sql.close()
                    return
            if edit_field == 2:
                suggest_password = input('Generate new random password? (y/n): ')
                if suggest_password == 'y':
                    new_pw = Hash_pass.random_password(16)
                else:
                    new_pw = input('Enter new password: ')
                if new_pw is not None:
                    encrypted_pw = aes.encrypt_data(new_pw)
                    try:
                        sql.edit_database(id=get, field='pass_hash', data=encrypted_pw)
                    except Exception as err:
                        print('Error editing entry:', err)
                    finally:
                        sql.close()

                else:
                    print('Error: password is None. ')
                    return False
    if args.delete:
        id_desc = sql.open_database()
        for i in id_desc:
            print('ID: ', i[0], "Description", i[1])
        get = input('Enter ID of entry to delete: ')
        try:
            get = int(get)
        except ValueError:
            print('Enter an integer!')
        else:
            if debug:
                print('Retrieving: ', get)
            ret = sql.delete_from_database(id=get)
            if ret:
                print(ret)
            else:
                exit(1)


if __name__ == "__main__":
    Hash_pass = lib.passlib.Hash_pass()
    master_pw = Hash_pass.get_master_password()
    aes = aes_lib.HandleAes(key=master_pw)
    main()
