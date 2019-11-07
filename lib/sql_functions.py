import sqlite3
from .clipw_conf import *


class Sql(object):
    def __init__(self):
        self.sqliteConnection = sqlite3.connect(database_file)

    def close(self):
        self.sqliteConnection.close()

    def init_database(self):
        sqliteConnection = self.sqliteConnection
        try:

            sqlite_create_table_query = '''CREATE TABLE Password_Store (
                                        id INTEGER PRIMARY KEY,
                                        desc text NOT NULL,
                                        pass_hash text NOT NULL);'''

            cursor = sqliteConnection.cursor()
            print("Successfully Connected to SQLite")
            cursor.execute(sqlite_create_table_query)
            sqliteConnection.commit()
            print("SQLite table created")



        except sqlite3.Error as error:
            print("Error while creating a sqlite table", error)
        #  finally:
            #  if (sqliteConnection):
                #  sqliteConnection.close()
                #  print("sqlite connection is closed")

    def edit_database(self, id, data, field):
        """
        Broken function to update a field of a row in the table
        :param id: primary key id for WHERE clause
        :param data: edited field data to replace in current db entry
        :param field: either desc (description) or pass_hash (password hash of entry)
        :return: True om success, false om fail
        """
        sqliteConnection = self.sqliteConnection
        try:
            cursor = sqliteConnection.cursor()  # define our sqlite connection
            print("Connected to SQLite")
            if field == 'pass_hash':  # updating password field
                cursor.execute('''Update Password_Store SET pass_hash = ? WHERE id = ?''',
                               (data, id))  # 2md failed method
            else:
                cursor.execute('''UPDATE Password_Store SET desc = ? WHERE id = ?''', (data, id))
            sqliteConnection.commit()
            print("Record Updated successfully ")
            #  cursor.close()
            return True

        except sqlite3.Error as error:
            print("Failed to update sqlite table", error)
            return False
        #finally:
            #if sqliteConnection:
                #sqliteConnection.close()
                #print("The SQLite connection is closed")

    def append_database(self, new_passwd, pw_description):
        """
        :param new_passwd:
        :param pw_description:
        :return:
        """
        sqliteConnection = self.sqliteConnection
        try:
            cursor = sqliteConnection.cursor()
            if debug:
                print("Connected to SQLite")
            dataCopy = cursor.execute("select count(*) from Password_Store")
            values = dataCopy.fetchone()
            id = int(values[0])
            sqlite_insert_with_param = """INSERT INTO 'Password_Store'
                              ('id', 'desc', 'pass_hash') 
                              VALUES (?, ?, ?);"""

            data_tuple = (id, pw_description, new_passwd)
            cursor.execute(sqlite_insert_with_param, data_tuple)
            sqliteConnection.commit()
            if debug:
                print("Python Variables inserted successfully into SqliteDb_developers table")

            # cursor.close()

        except sqlite3.Error as error:
            print("Failed to insert Python variable into sqlite table", error)
        else:
            print('Stored password ok.')
        #finally:
            #if sqliteConnection:
                #sqliteConnection.close()
                #if debug:
                    #print("The SQLite connection is closed")


    def open_database(self):
        """
        :param master_pw:
        :return:
        """
        sqliteConnection = self.sqliteConnection
        try:
            cursor = sqliteConnection.cursor()
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
            # cursor.close()
            return id_desc
        except sqlite3.Error as error:
            print("Failed to read data from sqlite table", error)
        #finally:
           #if sqliteConnection:
                #sqliteConnection.close()
                #if debug:
                    #print("The SQLite connection is closed")

    def select_from_db(self, id):
        """
        Grab a certain password from the database
        :param id: primary key of password to get
        :return: aes encrypted password
        """
        sqliteConnection = self.sqliteConnection
        try:
            cursor = sqliteConnection.cursor()
            if debug:
                print("Connected to SQLite")

            sql_select_query = """select * from Password_Store where id = ?"""
            cursor.execute(sql_select_query, (id,))
            record = cursor.fetchone()
            print("Retrieving ID ", id)
            # cursor.close()
            return record

        except sqlite3.Error as error:
            print("Failed to read data from sqlite table", error)
        #finally:
            #if sqliteConnection:
                #sqliteConnection.close()
                #if debug:
                    # print("The SQLite connection is closed")

    def delete_from_database(self, id):
        try:
            sqliteConnection = self.sqliteConnection
            cursor = sqliteConnection.cursor()
            if debug:
                print("Connected to SQLite")

            # Deleting single record now
            sql_delete_query = """DELETE from Password_Store where id = ?"""
            cursor.execute(sql_delete_query, (id,))
            sqliteConnection.commit()
            return ("Record deleted successfully ")
            #  cursor.close()

        except sqlite3.Error as error:
            print("Failed to delete record from sqlite table", error)
            return False
        # finally:
            #if (sqliteConnection):
                #sqliteConnection.close()
                # print("the sqlite connection is closed")
