#!/usr/env/bin python3

"""
Definition of the module to implement password hashing
"""
import bcrypt


def hash_password(password: str) -> bytes:
    """
    A function that hashes a password and returns a byte string
    """
    b = password.encode()
    hashed_password = bcrypt.hashpw(b, bcrypt.gensalt())
    return hashed_password


def is_valid(hashed_password: bytes, password: str) -> bool:
    """
    A function that validates a password
    """

    return bcrypt.checkpw(password.encode(), hashed_password)
