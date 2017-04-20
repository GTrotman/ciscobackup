import sys
import mysql.connector
from access import *


class sql:
    def __init__(self):
        self.db_host = dbhost
        self.db_port = 3306
        self.db_user = dbuser
        self.db_pass = dbpass
        self.db_name = 'liunetdev'
        # Create Database connection
        try:
            self.db_connect = mysql.connector.connect(host=self.db_host, port=self.db_port, user=self.db_user, password=self.db_pass, database=self.db_name)
            # Create cursor
            self.cursor = self.db_connect.cursor()
        except mysql.connector.Error as e:
            print(e.args)
            print("ERROR: %d: %s" % (e.args[0], e.args[1]))
            sys.exit(1)

    def request(self, sql):
        self.cursor.execute(sql)
        return self.cursor.fetchall()

    def close(self):
        # Close cursor
        self.cursor.close()
        # Close DB
        self.db_connect.close()
        print('Database connection closed')
