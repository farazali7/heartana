from hashlib import sha256
from hmac import compare_digest

SECRET_KEY = "bme 261"
AUTH_SIZE = 32


def sign(data):
    return sha256(data).hexdigest().encode('utf-8')


def verify(retrieved_data, signature):
    new_signature = sign(retrieved_data)
    return compare_digest(new_signature, signature)