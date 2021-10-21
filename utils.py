from passlib.hash import pbkdf2_sha256


def generate_hash(password):
    return pbkdf2_sha256.hash(password)


def verify_password(password, hashed_password):
    return pbkdf2_sha256.verify(password, hashed_password)
