#!/usr/bin/env python3
"""
function called filter_datum
that returns the log message obfuscated
"""

from typing import List
import re
import logging
import mysql.connector
from os import getenv


PII_FIELDS = ('name', 'password', 'phone', 'ssn', 'email')


def filter_datum(fields: List[str],
                 redaction: str,
                 message: str,
                 separator: str) -> str:
    """ return the log message obfuscated"""

    for x in fields:
        message = re.sub(x + "=.*?" + separator,
                         x + "=" + redaction + separator,
                         message)
    return message


class RedactingFormatter(logging.Formatter):
    """
    Redacting Formatter class
    """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        """The constructor"""
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """filter values in incoming log records using filter_datum"""

        return filter_datum(self.fields, self.REDACTION,
                            super(RedactingFormatter, self).format(record),
                            self.SEPARATOR)


def get_logger() -> logging.Logger:
    """
    function that takes no arguments
    and returns a logging.Logger object
    """
    log = logging.getLogger('user_data')
    log.setLevel(logging.INFO)
    log.propagate = False
    stream_handler = logging.StreamHandler()
    formater = RedactingFormatter(PII_FIELDS)
    log.setFormatter(formater)
    log.addHandler(stream_handler)

    return log


def get_db() -> mysql.connector.connection.MySQLConnection:
    """
    function that returns a connector to the database
    """
    db_conn = mysql.connector.connection.MySQLConnection(
        user=getenv('PERSONAL_DATA_DB_USERNAME', 'root'),
        password=getenv('PERSONAL_DATA_DB_PASSWORD', ''),
        host=getenv('PERSONAL_DATA_DB_HOST', 'localhost'),
        database=getenv('PERSONAL_DATA_DB_NAME')
    )

    return db_conn


def main():
    """Main function that handles user data"""
    my_db = get_db()
    cursor = my_db.cursor()
    cursor.execute("SELECT * FROM users;")
    fields = [i[0] for i in cursor.description]

    log = get_logger()

    for row in cursor:
        _row = ''.join(f'{f}={str(r)}; ' for r, f in zip(row, fields))
        log.info(_row.strip())

    cursor.close()
    my_db.close()


if __name__ == '__main__':
    main()
