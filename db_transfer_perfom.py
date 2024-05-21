import os
from db_conn import db_connection
from dotenv import load_dotenv
import requests
import logging

load_dotenv("api.env")
api_key = os.getenv("API_KEY")


@db_connection
def check_balance(cursor, sender_account_id, amount):
    cursor.execute("SELECT Amount, Currency FROM Account WHERE id = ?", (sender_account_id,))
    result = cursor.fetchone()
    if result:
        sender_balance, sender_currency = result
        if sender_balance >= amount:
            return True, sender_currency
        else:
            return False, sender_currency
    else:
        return False, None


@db_connection
def convert_currency(cursor, amount, sender_currency, receiver_currency):
    if sender_currency != receiver_currency:
        conversion_url = f"https://api.freecurrencyapi.net/v1/convert?apikey={api_key}&from={sender_currency}&to={receiver_currency}&amount={amount}"
        try:
            response = requests.get(conversion_url)
            response.raise_for_status()  # Raise an HTTPError if the HTTP request returned an unsuccessful status code
            return response.json().get('result')
        except requests.exceptions.RequestException as e:
            logging.error(f"Failed to convert currency: {e}")
            return None
    else:
        return amount


@db_connection
def perform_transaction(cursor, sender_account_id, receiver_account_id, amount):
    cursor.execute("UPDATE Account SET Amount = Amount - ? WHERE id = ?", (amount, sender_account_id))
    cursor.execute("UPDATE Account SET Amount = Amount + ? WHERE id = ?", (amount, receiver_account_id))


@db_connection
def update_transaction_history(cursor, sender_account_id, receiver_account_id, amount, sender_currency,
                               receiver_currency):
    cursor.execute(
        "INSERT INTO 'Transaction' (Bank_sender_name, Account_sender_id, Bank_receiver_name, Account_receiver_id, Sent_Currency, Sent_Amount, Receiver_Currency) VALUES (?, ?, ?, ?, ?, ?, ?)",
        ('Sender Bank', sender_account_id, 'Receiver Bank', receiver_account_id, sender_currency, amount,
         receiver_currency))


@db_connection
def transfer_money(cursor, sender_account_id, receiver_account_id, amount, receiver_currency):
    is_balance_sufficient, sender_currency = check_balance(sender_account_id, amount)

    if is_balance_sufficient:
        converted_amount = convert_currency(amount, sender_currency, receiver_currency)

        if converted_amount is not None:
            perform_transaction(sender_account_id, receiver_account_id, converted_amount)
            update_transaction_history(sender_account_id, receiver_account_id, amount, sender_currency,
                                       receiver_currency)

            logging.info("Money transfer successful")
            return True
        else:
            logging.error("Failed to convert currency")
            return False
    else:
        logging.error("Insufficient balance for the transaction")
        return False
