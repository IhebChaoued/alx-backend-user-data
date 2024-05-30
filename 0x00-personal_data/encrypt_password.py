#!/usr/bin/env python3
"""
Module for encrypting passwords
"""

import bcrypt


def hash_password(password: str) -> bytes:
    """Returns a salted, hashed password"""
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode(), salt)


def is_valid(hashed_password: bytes, password: str) -> bool:
    """Checks if the provided password matches the hashed password"""
    return bcrypt.checkpw(password.encode(), hashed_password)
