#!/usr/bin/env python3
"""
Auth module
"""
from db import DB
from user import User
import bcrypt
import uuid


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
        user = self._db.find_user_by(email=email)
        if user:
            hashed_password = user.hashed_password.encode('utf-8')
            return bcrypt.checkpw(password.encode('utf-8'), hashed_password)
        return False

    def _generate_uuid(self) -> str:
        """Generate a UUID string."""
        return str(uuid.uuid4())

    def create_session(self, email: str) -> str:
        """Create a new session for the user."""
        user = self._db.find_user_by(email=email)
        if user:
            session_id = self._generate_uuid()
            self._db.update_user(user.id, session_id=session_id)
            return session_id
        return None

    def get_user_from_session_id(self, session_id: str) -> User:
        """Retrieve the user corresponding to the given session ID."""
        if session_id is None:
            return None

        user = self._db.find_user_by(session_id=session_id)
        return user if user else None

    def destroy_session(self, user_id: int) -> None:
        """Destroy the session for the given user."""
        self._db.update_user(user_id, session_id=None)

    def get_reset_password_token(self, email: str) -> str:
        """Generate a reset password token for the user."""
        user = self._db.find_user_by(email=email)
        if not user:
            raise ValueError(f"User {email} does not exist")

        reset_token = self._generate_uuid()
        self._db.update_user(user.id, reset_token=reset_token)
        return reset_token

    def update_password(self, reset_token: str, password: str) -> None:
        """Update the password for the user using the reset token."""
        user = self._db.find_user_by(reset_token=reset_token)
        if not user:
            raise ValueError("Invalid reset token")

        hashed_password = _hash_password(password)
        self._db.update_user(
                user.id, hashed_password=hashed_password, reset_token=None
                )
