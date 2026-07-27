""" SQL DB access helper. Using sqlite3 for demo."""
import sqlite3
from sqlite3 import Error

def create_connection(path):
    """Create DB connection."""
    connection = None
    try:
        connection = sqlite3.connect(path)
        print("Connection to SQLite DB successful")
    except Error as e:
        print(f"The error '{e}' occurred")

    return connection

def execute_read_query(connection, query):
    """Execute SQL query and return result."""
    cursor = connection.cursor()
    result = None
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        return result
    except Error as e:
        print(f"The error '{e}' occurred")
