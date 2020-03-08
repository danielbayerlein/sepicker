import logging
import mysql.connector as mysql

LOGGER = logging.getLogger(__name__)


class Mysql:
    def __init__(self, user, password, host, database):
        self.user = user
        self.password = password
        self.host = host
        self.database = database

    def __enter__(self):
        self.connection = mysql.connect(
            user=self.user,
            password=self.password,
            host=self.host,
            database=self.database
        )
        self.cursor = self.connection.cursor()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.connection.commit()
        self.cursor.close()
        self.connection.close()

    def save(self, values):
        self.cursor.executemany(
            'INSERT INTO sepicker(timestamp, name, value) VALUES(%s, %s, %s)',
            values
        )
