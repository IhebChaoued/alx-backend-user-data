#!/usr/bin/env python3
"""
Module for filtering log messages and connecting to a secure database.
"""

import re
import logging
from typing import List
import os
import mysql.connector
from mysql.connector import connection


def filter_datum(
        fields: List[str],
        redaction: str,
        message: str,
        separator: str
        ) -> str:
    """Obfuscates specified fields in the log message"""
    pattern = '|'.join([f'{field}=[^\\{separator}]*' for field in fields])
    return re.sub(
        pattern,
        lambda m: m.group(0).split('=')[0] + f'={redaction}',
        message
    )


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class """
    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        """Initialize the formatter with fields to redact"""
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """Format the log record to redact sensitive fields"""
        message = super(RedactingFormatter, self).format(record)
        return filter_datum(
            self.fields,
            self.REDACTION,
            message,
            self.SEPARATOR
        )


PII_FIELDS = ("name", "email", "phone", "ssn", "password")


def get_logger() -> logging.Logger:
    """Creates a logger with specified settings"""
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    logger.propagate = False
    handler = logging.StreamHandler()
    formatter = RedactingFormatter(fields=PII_FIELDS)
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger


def get_db() -> connection.MySQLConnection:
    """Returns a connection to the database"""
    username = os.getenv("PERSONAL_DATA_DB_USERNAME", "root")
    password = os.getenv("PERSONAL_DATA_DB_PASSWORD", "")
    host = os.getenv("PERSONAL_DATA_DB_HOST", "localhost")
    database = os.getenv("PERSONAL_DATA_DB_NAME")

    return mysql.connector.connect(
        user=username,
        password=password,
        host=host,
        database=database
    )


def main() -> None:
    """Retrieves all rows in the users table and displays them"""
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM users;")
    logger = get_logger()

    for row in cursor:
        message = (
            f"name={row[0]}; email={row[1]}; phone={row[2]}; "
            f"ssn={row[3]}; password={row[4]}; ip={row[5]}; "
            f"last_login={row[6]}; user_agent={row[7]};"
        )
        logger.info(message)

    cursor.close()
    db.close()


if __name__ == "__main__":
    main()
