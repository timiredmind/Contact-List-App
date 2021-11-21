from passlib.hash import pbkdf2_sha256
from marshmallow import ValidationError
import re
from urllib.parse import urlencode
from flask import request
from extension import cache


def generate_hash(password):
    return pbkdf2_sha256.hash(password)


def verify_password(password, hashed_password):
    return pbkdf2_sha256.verify(password, hashed_password)


# Custom validator
def validate_phone_number(phone_number):
    if not re.search(r"^0[0-9]{10}$", phone_number):
        raise ValidationError("Invalid Phone Number")


def generate_url(page, per_page):
    query_args = request.args.to_dict()
    query_args["page"] = page
    query_args["per_page"] = per_page
    return f"{request.base_url}?{urlencode(query_args)}"


def clear_cache(key_prefix):
    key_list = [key for key in cache.cache._cache().keys if key.startswith(key_prefix)]
    cache.delete_many(*key_list)

