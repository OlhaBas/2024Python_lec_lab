import sqlite3
import logging


def db_connection(func):
    def wrapper(*args, **kwargs):
        conn = sqlite3.connect('bank_database.db')
        cursor = conn.cursor()
        try:
            result = func(cursor, *args, **kwargs)
            conn.commit()
            logging.info(f"Successfully executed {func.__name__}")
            return result

        except Exception as e:
            conn.rollback()
            logging.error(f"Error executing {func.__name__}: {str(e)}")
            return "Failure: " + str(e)
        finally:
            conn.close()

    return wrapper
