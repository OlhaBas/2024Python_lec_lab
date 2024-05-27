import random
import sqlite3
import logging
import datetime
from db_conn import db_connection


logger = logging.getLogger(__name__)


@db_connection
def providing_random_discounts_for_users(cursor):
    try:
        cursor.execute("SELECT Id FROM 'User'")
        users = cursor.fetchall()

        num_users_to_select = min(len(users), random.randint(1, 10))

        selected_users = random.sample(users, num_users_to_select)
        possible_discounts = [25, 30, 50]

        user_discounts = {}
        for user in selected_users:
            user_id = user[0]
            discount = random.choice(possible_discounts)
            user_discounts[user_id] = discount
        logger.info(f"Selected users with discounts: {user_discounts}")

        return user_discounts
    except sqlite3.Error as e:
        logger.error(f"Database error: {e}")
        return {}
    except Exception as e:
        logger.error(f"Error: {e}")
        return {}


@db_connection
def searching_users_with_debts(cursor):
    try:
        cursor.execute("""
            SELECT Name, Surname
            FROM User
            WHERE Id IN (
                SELECT DISTINCT User_id
                FROM Account
                WHERE Amount < 0
            )
        """)
        users = cursor.fetchall()
        return users
    except Exception as e:
        logging.error(f"Error fetching users with debts: {str(e)}")
        return []


@db_connection
def searching_bank_highest_capital(cursor):
    try:
        cursor.execute("""
            SELECT Bank.bank_name
            FROM Bank
            JOIN Account ON Bank.id = Account.Bank_id
            GROUP BY Bank.id
            ORDER BY SUM(Account.Amount) DESC
            LIMIT 1
        """)
        bank = cursor.fetchone()
        return bank[0] if bank else None
    except Exception as e:
        logging.error(f"Error fetching bank with highest capital: {str(e)}")
        return None


@db_connection
def searching_bank_serving_oldest_client(cursor):
    try:
        cursor.execute("""
            SELECT Bank.bank_name
            FROM Bank
            JOIN Account ON Bank.id = Account.Bank_id
            JOIN User ON Account.User_id = User.Id
            WHERE User.Birthday IS NOT NULL
            ORDER BY User.Birthday ASC
            LIMIT 1
        """)
        bank = cursor.fetchone()
        return bank[0] if bank else None
    except Exception as e:
        logging.error(f"Error fetching bank serving oldest client: {str(e)}")
        return None


@db_connection
def searching_bank_with_outgoing_transactions(cursor):
    try:
        cursor.execute("""
            SELECT Bank.bank_name
            FROM Bank
            JOIN Account ON Bank.id = Account.Bank_id
            JOIN 'Transaction' ON Account.id = 'Transaction'.Account_sender_id
            GROUP BY Bank.id
            ORDER BY COUNT(DISTINCT 'Transaction'.Account_sender_id) DESC
            LIMIT 1
        """)
        bank = cursor.fetchone()
        return bank[0] if bank else None
    except Exception as e:
        logging.error(f"Error fetching bank with most outgoing transactions: {str(e)}")
        return None


@db_connection
def deleting_incomplete_users_and_accounts(cursor):
    try:
        cursor.execute("""
            DELETE FROM Account
            WHERE User_id IN (
                SELECT Id
                FROM User
                WHERE Name IS NULL OR Surname IS NULL OR Birthday IS NULL OR Account IS NULL
            )
        """)
        cursor.execute("""
            DELETE FROM User
            WHERE Name IS NULL OR Surname IS NULL OR Birthday IS NULL OR Account IS NULL
        """)
        return "Successfully deleted incomplete users and accounts"
    except Exception as e:
        logging.error(f"Error deleting incomplete users and accounts: {str(e)}")
        return f"Error deleting incomplete users and accounts: {str(e)}"



@db_connection
def searching_user_transactions_last_3_months(cursor, user_id):
    try:
        three_months_ago = datetime.datetime.now() - datetime.timedelta(days=90)

        cursor.execute("""
            SELECT *
            FROM 'Transaction'
            WHERE Account_sender_id = ? AND Datetime >= ?
        """, (user_id, three_months_ago))
        transactions = cursor.fetchall()
        return transactions
    except Exception as e:
        logging.error(f"Error fetching user transactions for last 3 months: {str(e)}")
        return []
