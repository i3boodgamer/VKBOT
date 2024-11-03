import re


def is_valid_phone_number(phone_number: str):
    if re.match(r'^[78]\d{10}$', phone_number):
        if phone_number.startswith('8'):
            phone_number = '7' + phone_number[1:]
        return phone_number
    else:
        return None