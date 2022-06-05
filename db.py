import sqlite3
from sqlite3 import Error


class DB:
    def __init__(self, db_file):
        self.db_file = db_file
        self.conn = None
        self.create_all_tables()

    def create_connection(self) -> None:
        """ create a database connection to the SQLite database
            specified by db_file
        :return: None
        """
        try:
            self.conn = sqlite3.connect(self.db_file)
            self.conn.row_factory = sqlite3.Row
        except Error as e:
            print(e)

        return self.conn

    def close_connection(self):
        """ close database connection
        :return:
        """
        try:
            self.conn.close()
        except Error as e:
            print(e)

        return self.conn

    def create_table(self, create_table_sql):
        """ create a table from the create_table_sql statement
        :param create_table_sql: a CREATE TABLE statement
        :return:
        """
        try:
            c = self.conn.cursor()
            c.execute(create_table_sql)
        except Error as e:
            print(e)

    def create_all_tables(self):
        sql_create_phones_table = """CREATE TABLE IF NOT EXISTS phones (
                                            phoneID integer PRIMARY KEY,
                                            contactName text NOT NULL,
                                            phoneValue integer NOT NULL                                        
                                        );"""
        self.create_connection()
        self.create_table(create_table_sql=sql_create_phones_table)
        self.close_connection()
