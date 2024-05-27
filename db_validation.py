import re
import datetime


def validating_user_full_name(name, surname):
    name_matches = re.findall(r'[a-zA-Z]+', name)
    surname_matches = re.findall(r'[a-zA-Z]+', surname)

    if not re.fullmatch(r'[a-zA-Z ]+', name) or not re.fullmatch(r'[a-zA-Z ]+', surname):  # Function just for checking
        raise ValueError("Invalid characters in name or surname")

    validated_name = ' '.join(name_matches)
    validated_surname = ' '.join(surname_matches)

    return validated_name, validated_surname


def validating_field_value(field_name, value, valid_values):  # Validation for account and currency
    if value not in valid_values:
        raise ValueError(f"Invalid value '{value}' for field '{field_name}'! Must be one of {valid_values}")


def validating_datetime(transaction_datetime):
    if transaction_datetime is None:
        return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    else:
        return transaction_datetime


def validating_account_number(account_number):
    account_number = re.sub(r'[#%_?&]', '-', account_number)
    if len(account_number) != 18:
        raise ValueError("Account number should be a string of 18 characters!")
    if not account_number.startswith("ID--"):
        raise ValueError("Account number should begin with 'ID--'!")
    pattern = r'ID--[a-zA-Z]{1}-\d{1}-\d{7}-[a-zA-Z]{1}\d{1}'
    if not re.fullmatch(pattern, account_number):
        raise ValueError("Account number should contain the desired pattern!")
    return account_number

    # r'[a-zA-Z]{1,3}-\d+-\d+-'
