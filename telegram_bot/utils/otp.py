import random


def generate_otp() -> str:
    digits = '0123456789'
    code = ''.join(random.choices(digits, k=6))
    return code
