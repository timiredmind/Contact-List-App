from passlib.hash import pbkdf2_sha256
from marshmallow import ValidationError
import re


def generate_hash(password):
    return pbkdf2_sha256.hash(password)


def verify_password(password, hashed_password):
    return pbkdf2_sha256.verify(password, hashed_password)


# Custom validator
def validate_phone_number(phone_number):
    if len(phone_number) != 11:
        raise ValidationError("Phone number should have 11 digits")
    if not re.search(r"^0[0-9]{10}$", phone_number):
        raise ValidationError("Invalid Phone Number")
