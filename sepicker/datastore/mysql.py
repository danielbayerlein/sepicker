import logging
import mysql.connector as mysql
from ..config import (DB_USER, DB_PASSWORD, DB_HOST, DB_DATABASE)

LOGGER = logging.getLogger(__name__)


def save(values):
    connection = mysql.connect(
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        database=DB_DATABASE
    )
    cursor = connection.cursor()
    cursor.executemany(
        'INSERT INTO canable_test(timestamp, name, value) VALUES(%s, %s, %s)',
        values
    )
    connection.commit()
    cursor.close()
    connection.close()

# import traceback
# LOG.warning('Unable to run Lambda function on API Gateway message: %s %s' % (e, traceback.format_exc()))
