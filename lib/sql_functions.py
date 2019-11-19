import sqlite3
from sqlite3.dbapi2 import Connection

from .clipw_conf import *
from typing import Union


class Sql:
    """
    Wrapper object to handle sqlite functions
    """

    def __init__(self):
        self.database_file = database_file

    def open(self) -> Connection:
        """
            Connect to SQL database
        """
        try:
            self.sqlite_connection = sqlite3.connect(self.database_file)
        except Exception as err:
            print('Error connecting to database:', err)
        else:
            return self.sqlite_connection

    def close(self) -> bool:
        """
        Close connection to SQL database
        :return:
        """
        try:
            self.sqlite_connection.close()
        except Exception as err:
            print('Error closing database:', err)
            return False

    def init_database(self) -> bool:
        """
        Function to init database on first run.
        :return:
        """
        sqlite_connection = self.open()
        try:

            sqlite_create_table_query = '''CREATE TABLE Password_Store (
                                        id INTEGER PRIMARY KEY,
                                        desc text NOT NULL,
                                        pass_hash text NOT NULL);'''

            cursor = sqlite_connection.cursor()
            print("Successfully Connected to SQLite")
            cursor.execute(sqlite_create_table_query)
            sqlite_connection.commit()
            print("SQLite table created")
            return True

        except sqlite3.Error as error:
            print("Error while creating a sqlite table:", error)
            return False
        finally:
            self.close()

    def edit_database(self, id_, data, field) -> Union[bool, str]:
        """
        FIXED Function to update a field of a row in the table
        :param id_: primary key id for WHERE clause
        :param data: edited field data to replace in current db entry
        :param field: either desc (description) or pass_hash (password hash of entry)

        :return: bool
        """

        sqlite_connection = self.open()
        try:
            cursor = sqlite_connection.cursor()  # define our sqlite connection
            print("Connected to SQLite")
            if field == 'pass_hash':  # updating password field
                cursor.execute('''Update Password_Store SET pass_hash = ? WHERE id = ?''',
                               (data, id_))  # 2md failed method
            else:
                cursor.execute('''UPDATE Password_Store SET desc = ? WHERE id = ?''', (data, id_))
            sqlite_connection.commit()
            print("Record Updated successfully ")
            return True

        except sqlite3.Error as error:
            print("Failed to update sqlite table", error)
            return False
        finally:
            self.close()

    def append_database(self, new_passwd, pw_description) -> bool:
        """
        :param new_passwd: entry's password to append
        :param pw_description: entry's password description to append

        :return:
        """
        #  sqlite_connection = self.sqlite_connection
        sqlite_connection = self.open()
        try:
            cursor = sqlite_connection.cursor()
            if debug:
                print("Connected to SQLite")
            data_copy = cursor.execute("select count(*) from Password_Store")
            values = data_copy.fetchone()
            id_ = int(values[0])
            sqlite_insert_with_param = """INSERT INTO 'Password_Store'
                              ('id', 'desc', 'pass_hash') 
                              VALUES (?, ?, ?);"""
            attempts = 1  # Make sure that ID is unique
            while True:
                try:
                    data_tuple = (id_ + attempts, pw_description, new_passwd)
                    cursor.execute(sqlite_insert_with_param, data_tuple)
                except sqlite3.Error:
                    attempts += 1
                else:
                    sqlite_connection.commit()
                    break

            if debug:
                print("Python Variables inserted successfully into SqliteDb_developers table")

        except sqlite3.Error as error:
            print("Failed to insert Python variable into sqlite table:", error)
            return False
        else:
            print('Stored password ok.')
        finally:
            self.close()

    def open_database(self) -> Union[list, bool]:
        """
        Open the database

        :return: list(entries in database)
        """
        #  sqlite_connection = self.sqlite_connection
        sqlite_connection = self.open()
        try:
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
            return id_desc
        except sqlite3.Error as error:
            print("Failed to read data from sqlite table", error)
            return False
        except Exception as err:
            print('Unknown error:', err)
        finally:
            self.close()

    def select_from_db(self, id_: int) -> Union[list, bool]:
        """
        Grab a certain password from the database
        :rtype: object
        :param id_: primary key of password to get

        :return: aes encrypted password
        """
        # sqlite_connection = self.sqlite_connection
        sqlite_connection = self.open()
        try:
            cursor = sqlite_connection.cursor()
            if debug:
                print("Connected to SQLite")

            sql_select_query = """select * from Password_Store where id = ?"""
            cursor.execute(sql_select_query, (id_,))
            record = cursor.fetchone()
            if debug:
                print("Sql library: Retrieving ID:", id_)
            return record

        except sqlite3.Error as error:
            print("Failed to read data from sqlite table", error)
            return False
        finally:
            self.close()

    def delete_from_database(self, id_) -> Union[str, bool]:
        """
        Delete an entry from the database
        :param id_: primary key id

        :return: str or False
        """
        sqlite_connection = self.open()
        try:
            cursor = sqlite_connection.cursor()
            if debug:
                print("Connected to SQLite")
            # Deleting single record now
            sql_delete_query = """DELETE from Password_Store where id = ?"""
            cursor.execute(sql_delete_query, (id_,))
            sqlite_connection.commit()
            return "Record deleted successfully "

        except sqlite3.Error as error:
            print("Failed to delete record from sqlite table", error)
            return False
        finally:
            self.close()
