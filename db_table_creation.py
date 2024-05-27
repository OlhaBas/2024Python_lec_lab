import logging
import argparse
import sys
from db_conn import db_connection

logger = logging.getLogger(__name__)


@db_connection
def creating_database(cursor, enable_uniqueness):
    logging.basicConfig(filename='db_sql.log', level=logging.INFO)

    cursor.execute('''CREATE TABLE IF NOT EXISTS Bank (
                        id INTEGER PRIMARY KEY,
                        bank_name TEXT NOT NULL UNIQUE
                    )''')
    logger.info('Database table "Bank" created')

    cursor.execute('''CREATE TABLE IF NOT EXISTS 'Transaction' (
                        id INTEGER PRIMARY KEY,
                        Bank_sender_name TEXT NOT NULL,
                        Account_sender_id INTEGER NOT NULL,
                        Bank_receiver_name TEXT NOT NULL,
                        Account_receiver_id INTEGER NOT NULL,
                        Sent_Currency TEXT NOT NULL,
                        Sent_Amount REAL NOT NULL,
                        Receiver_Currency TEXT,
                        Sender_Currency TEXT,
                        Datetime TEXT
                    )''')
    logger.info('Database table "Transaction" created')

    if enable_uniqueness:
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS 'User' (
            Id INTEGER PRIMARY KEY,
            'Name' TEXT NOT NULL,
            Surname TEXT NOT NULL,
            Birthday TEXT,
            Account TEXT NOT NULL,
            UNIQUE('Name', Surname) ON CONFLICT IGNORE,
            FOREIGN KEY(Account) REFERENCES 'Account'(Account_Number)
        )
        """)
        logger.info('Database table "User" with enabled uniqueness created')
    else:
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS 'User' (
            Id INTEGER PRIMARY KEY,
            'Name' TEXT NOT NULL,
            Surname TEXT NOT NULL,
            Birthday TEXT,
            Account TEXT NULL,
            FOREIGN KEY(Account) REFERENCES Account(Account_Number)
        )
        """)
        logger.info('Database table "User"  with disabled uniqueness created')

    cursor.execute('''CREATE TABLE IF NOT EXISTS 'Account' (
                        id INTEGER PRIMARY KEY,
                        User_id INTEGER NOT NULL,
                        'Type' TEXT NOT NULL,
                        Account_Number TEXT NOT NULL UNIQUE,
                        Bank_id INTEGER NOT NULL,
                        Currency TEXT NOT NULL,
                        Amount REAL NOT NULL,
                        Status TEXT,
                        FOREIGN KEY(User_id) REFERENCES 'User'(Id),
                        FOREIGN KEY(Bank_id) REFERENCES Bank(id)
                    )''')
    logger.info('Database table "Account" created')


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Initial database setup script')
    parser.add_argument('--unique-constraints', dest='unique_constraints', action='store_true',
                        help='Toggle uniqueness constraints on User.Name and User.Surname')
    parser.add_argument('--no-unique-constraints', dest='unique_constraints', action='store_false',
                        help='Disable uniqueness constraints on User.Name and User.Surname')
    parser.set_defaults(unique_constraints=True)
    args = parser.parse_args()

    creating_database(args.unique_constraints, )

    script_name = sys.argv[0]
    print("Name of script :", script_name)
