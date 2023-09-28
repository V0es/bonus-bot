import logging
import random


def generate_otp() -> str:
    digits = '0123456789'
    code = ''.join(random.choices(digits, k=4))
    logging.info('Generated new OTP')
    return code
