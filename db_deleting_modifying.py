import logging
from db_conn import db_connection



@db_connection
def modifying_user(cursor, user_id, new_data):
    try:
        cursor.execute('''UPDATE User SET Name=?, Surname=?, Birthday=?, Account=? WHERE User_id=?''',
                       (new_data['Name'], new_data['Surname'], new_data['Birthday'], new_data['Account'], user_id))
        return "Success: User data updated"
    except Exception as e:
        logging.error(f"Error modifying user data: {e}")
        return f"Error: {e}"


@db_connection
def modifying_bank(cursor, bank_id, new_data):
    try:
        cursor.execute('''UPDATE Bank SET bank_name=? WHERE Bank_id=?''',
                       (new_data['bank_name'], bank_id))
        return "Success: Bank data updated"
    except Exception as e:
        logging.error(f"Error modifying bank data: {e}")
        return f"Error: {e}"


@db_connection
def modifying_account(cursor, account_id, new_data):
    try:
        cursor.execute('''UPDATE Account SET Type=?, Account_Number=?, Bank_id=?, Currency=?, Amount=?, Status=? 
                          WHERE Account_id=?''',
                       (new_data['Type'], new_data['Account_Number'], new_data['Bank_id'], new_data['Currency'],
                        new_data['Amount'], new_data['Status'], account_id))
        return "Success: Account data updated"
    except Exception as e:
        logging.error(f"Error modifying account data: {e}")
        return f"Error: {e}"


@db_connection
def deleting_user(cursor, user_id):

    try:
        cursor.execute('''DELETE FROM User WHERE User_id=?''', (user_id,))
        return "Success: User deleted"
    except Exception as e:
        logging.error(f"Error deleting user: {e}")
        return f"Error: {e}"


@db_connection
def deleting_bank(cursor, bank_id):

    try:
        cursor.execute('''DELETE FROM Bank WHERE Bank_id=?''', (bank_id,))
        return "Success: Bank deleted"
    except Exception as e:
        logging.error(f"Error deleting bank: {e}")
        return f"Error: {e}"


@db_connection
def deleting_account(cursor, account_id):

    try:
        cursor.execute('''DELETE FROM Account WHERE Account_id=?''', (account_id,))
        return "Success: Account deleted"
    except Exception as e:
        logging.error(f"Error deleting account: {e}")
        return f"Error: {e}"