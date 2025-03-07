from datetime import datetime
import logging
import mysql.connector as mysql

logger = logging.getLogger(__name__)


class Mysql:
    def __init__(self, user: str, password: str, host: str, database: str):
        self.user = user
        self.password = password
        self.host = host
        self.database = database

    def __enter__(self) -> 'Mysql':
        self.connection = mysql.connect(
            user=self.user,
            password=self.password,
            host=self.host,
            database=self.database
        )
        self.cursor = self.connection.cursor()
        return self

    def __exit__(
        self,
        exc_type: type,
        exc_val: Exception,
        exc_tb: type
    ):
        self.connection.commit()
        self.cursor.close()
        self.connection.close()

    def save(self, values: list[tuple[datetime, str, int | str]]) -> None:
        self.cursor.executemany(
            'INSERT INTO sepicker(timestamp, name, value) VALUES(%s, %s, %s)',
            values
        )
