import re


def is_valid_phone_number(phone_number: str):
    pattern = re.compile(r'^7\d{10}$')
    return pattern.match(phone_number) is not None