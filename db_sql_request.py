import csv
import logging
from db_transfer_perfom import transfer_money
from db_conn import db_connection
from db_validation import validating_user_full_name, validating_field_value, validating_datetime, validating_account_number
from db_deleting_modifying import modifying_user, modifying_bank, modifying_account, deleting_user, deleting_bank, deleting_account
from db_random_task import providing_random_discounts_for_users, searching_users_with_debts, searching_bank_highest_capital, searching_bank_serving_oldest_client, searching_bank_serving_oldest_client, searching_bank_with_outgoing_transactions, deleting_incomplete_users_and_accounts, searching_user_transactions_last_3_months

logging.basicConfig(filename='db_interaction.log', level=logging.INFO, format= '%(asctime)s - %(name)s - %(levelname)s - %(message)s')


@db_connection
def adding_user(cursor, name, surname, birthday, account):
    try:
        validated_name, validated_surname = validating_user_full_name(name, surname)
    except ValueError as e:
        logging.error(f"Error validating user full name: {e}")
        return f"Error: {e}"

    if not validated_name or not validated_surname:
        return "Error: Invalid characters in name or surname"

    cursor.execute('''SELECT * FROM User WHERE Name=? AND Surname=?''', (validated_name, validated_surname))
    existing_user = cursor.fetchone()
    if existing_user:
        return "Error: User with the same name and surname already exists"
    else:
        cursor.execute('''INSERT INTO User (Name, Surname, Birthday, Account) 
                          VALUES (?, ?, ?, ?)''', (validated_name, validated_surname, birthday, account))
        return "Success: User added to the database"


@db_connection
def adding_bank(cursor, bank_name):
    cursor.execute('''SELECT * FROM Bank WHERE bank_name=?''', (bank_name,))
    existing_bank = cursor.fetchone()
    if existing_bank:
        return "Error: Bank with the same name already exists"
    else:
        cursor.execute('''INSERT INTO Bank (bank_name) VALUES (?)''', (bank_name,))
        return "Success: Bank added to the database"


@db_connection
def adding_account(cursor, user_id, type, account_number, bank_id, currency, amount, status=None):
    try:
        validated_account_number = validating_account_number(account_number)

        # Validate the type and currency fields
        valid_account_types = ['Credit', 'Debit']
        valid_currencies = ['USD', 'EUR', 'GBP']
        valid_status = ['Golden', 'Silver', 'Platinum']
        validating_field_value('Type', type, valid_account_types)
        validating_field_value('Currency', currency, valid_currencies)
        validating_field_value('Status', status, valid_status)

    except ValueError as e:
        logging.error(f"Error validating account number: {e}")
        return f"Error: {e}"

    cursor.execute('''SELECT * FROM Account WHERE Account_Number=?''', (account_number,))
    existing_account = cursor.fetchone()
    if existing_account:
        return "Error: Account with the same account number already exists"
    else:
        if status is None:
            cursor.execute('''INSERT INTO Account (User_id, Type, Account_Number, Bank_id, Currency, Amount) 
                              VALUES (?, ?, ?, ?, ?, ?)''',
                           (user_id, type, validated_account_number, bank_id, currency, amount))
        else:
            cursor.execute('''INSERT INTO Account (User_id, Type, Account_Number, Bank_id, Currency, Amount, Status) 
                              VALUES (?, ?, ?, ?, ?, ?, ?)''',
                           (user_id, type, validated_account_number, bank_id, currency, amount, status))
        return "Success: Account added to the database"


@db_connection
def adding_data_csv(cursor):
    with open('user.csv', newline='') as user_file, \
            open('account.csv', newline='') as account_file, \
            open('transaction.csv', newline='') as transaction_file, \
            open('bank.csv', newline='') as bank_file:

        user_reader = csv.DictReader(user_file)
        account_reader = csv.DictReader(account_file)
        transaction_reader = csv.DictReader(transaction_file)
        bank_reader = csv.DictReader(bank_file)

        for row in user_reader:
            cursor.execute("INSERT INTO User (Name, Surname, Birthday, Account) VALUES (?, ?, ?, ?)",
                           (row['Name'], row['Surname'], row['Birthday'], row['Account']))

        for row in account_reader:

            try:
                # Validate the type and currency fields
                valid_account_types = ['Credit', 'Debit']
                valid_currencies = ['USD', 'EUR', 'GBP']
                valid_status = ['Golden', 'Silver', 'Platinum']
                validating_field_value('Type', row['Type'], valid_account_types)
                validating_field_value('Currency', row['Currency'], valid_currencies)
                validating_field_value('Status', row['Status'], valid_status)

            except ValueError as e:
                logging.error(f"Error validating account number: {e}")
                continue  # Gonna skip this row if validation fails

            cursor.execute(
                "INSERT INTO Account (User_id, Type, Account_Number, Bank_id, Currency, Amount, Status) VALUES (?, ?, "
                "?, ?, ?, ?, ?)",
                (row['User_id'], row['Type'], row['Account_Number'], row['Bank_id'], row['Currency'], row['Amount'],
                 row['Status']))

        for row in transaction_reader:
            validated_datetime = validating_datetime(row['Datetime'])
            cursor.execute(
                "INSERT INTO 'Transaction' (Bank_sender_name, Account_sender_id, Bank_receiver_name, "
                "Account_receiver_id, Sent_Currency, Sent_Amount, Datetime, Receiver_currency, Sender_currency) "
                "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                (row['Bank_sender_name'], row['Account_sender_id'], row['Bank_receiver_name'],
                 row['Account_receiver_id'], row['Sent_Currency'], row['Sent_Amount'], validated_datetime,
                 row['Receiver_currency'], row['Sender_currency']))

        for row in bank_reader:
            cursor.execute("INSERT INTO Bank (bank_name) VALUES (?)",
                           (row['bank_name'],))


if __name__ == "__main__":
    # Example usage omg
    adding_data_csv()
    adding_user("Lilith", "Mark", "1999-11-16", 7, )
    adding_bank("BankFromScript", )
    adding_account(7, "Credit", "ID--Z-2-2121122-D4", 5, "GBP", 2211, "Golden")
    transfer_money("1", "2", 500.0, "USD")


    #modify_user(1, {'Name': 'New Name', 'Surname': 'New Surname', 'Birthday': '1990-01-01', 'Account': 'New Account'})
    #modify_bank(1, {'bank_name': 'New Bank Name'})
    #modify_account(1, {'Type': 'New Type', 'Account_Number': 'New Account Number', 'Bank_id': 123,
                         #'Currency': 'New Currency', 'Amount': 1000, 'Status': 'New Status'})

    #delete_user(123)
    #delete_bank(456)
    #delete_account(789)

    # dict with function and discription
    functions = {
        providing_random_discounts_for_users: "Random discounts forusers",
        searching_users_with_debts: "Users with debts",
        searching_bank_highest_capital: "Bank with highest capital",
        searching_bank_serving_oldest_client: "Bank serving oldest client",
        searching_bank_with_outgoing_transactions: "Bank with most outgoing transactions",
        deleting_incomplete_users_and_accounts: "Delete incomplete users and accounts",
        searching_user_transactions_last_3_months: "User transactions last 3 months",
    }

    # calling a function ang its logging
    for func, description in functions.items():
        try:
            if func == searching_user_transactions_last_3_months:
                result = func(1) #user_id here, I can pick whenever user is required
            else:
                result = func()
            logging.info(f"{description}: {result}")
        except Exception as e:
            logging.error(f"Error executing {description}: {str(e)}")

