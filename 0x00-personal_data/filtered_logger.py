#!/usr/bin/env python3
from typing import List
import re


"""
function that returns the log message obfuscated
"""

def filter_datum(
    fields: List[str],
    redaction: str,
    message: str,
    separator: str) -> str:
    """ return the log message obfuscated"""

    for x in fields:
        message = re.sub(x + "=.*?" + separator,
                         x + "=" + redaction + separator,
                         message)
    return message
