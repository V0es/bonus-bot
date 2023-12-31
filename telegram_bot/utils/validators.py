import re


def validate_phone_number(phone_number: str) -> bool:
    regexp = '^\+\d{1,3}\d{3}\d{7}$'
    if len(re.findall(regexp, phone_number)) == 1:
        return True
    else:
        return False


def validate_email(email: str) -> bool:
    regexp = '^[^@\s]+@[^@\s]+\.[^@\s]+'
    if len(re.findall(regexp, email)) == 1:
        return True
    else:
        return False


def validate_fullname(fullname: str) -> bool:
    forbidden_symbols = '[]{}+=&^:;\|/><$#@!?№%()'
    for symbol in forbidden_symbols:
        if symbol in fullname:
            return False
    return True


def validate_order_amount(amount: str) -> bool:
    return amount.isdigit()
