#!/usr/bin/env python3
"""
Auth module
"""
from db import DB
from user import User
import bcrypt


def _hash_password(password: str) -> bytes:
    """Hash a password with bcrypt."""
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())


class Auth:
    """Auth class to interact with the authentication database."""

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """Register a new user with the provided email and password."""
        try:
            self._db.find_user_by(email=email)
            raise ValueError(f"User {email} already exists")
        except NoResultFound:
            hashed_password = _hash_password(password)
            new_user = self._db.add_user(email, hashed_password)
            return new_user

    def valid_login(self, email: str, password: str) -> bool:
        """Validate login credentials."""
        try:
            user = self._db.find_user_by(email=email)
            stored_password = user.hashed_password
            return bcrypt.checkpw(password.encode('utf-8'), stored_password)
        except NoResultFound:
            return False
