import hashlib
import secrets
import time
from CPR_Banking.com.repo.db_operations import *


def hash_password_with_salt(salt,password):
    # Generate a random salt
    #salt = secrets.token_hex(16)  # 16 bytes of random data

    # Concatenate the salt and password
    salted_password = str(salt) + password

    # Hash the salted password using SHA-256
    hashed_password = hashlib.sha256(salted_password.encode()).hexdigest()

    # Return the salt and hashed password as a tuple
    return hashed_password


