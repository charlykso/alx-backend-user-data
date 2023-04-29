#!/usr/bin/env python3
from typing import List
import re
import logging


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

    def __init__(self):
        """The constructor"""
        super(RedactingFormatter, self).__init__(self.FORMAT)

    def format(self, record: logging.LogRecord) -> str:
        """filter values in incoming log records using filter_datum"""

        return filter_datum(self.fields, self.REDACTION,
                            super(RedactingFormatter, self).format(record),
                            self.SEPARATOR)
