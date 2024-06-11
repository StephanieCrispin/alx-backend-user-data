#!/usr/bin/env python3
'''Defines authentication functions'''
from db import DB
import bcrypt
from bcrypt import hashpw
from user import User
import uuid


def _hash_password(password: str) -> bytes:
    """Functions that hashes the input to bytes"""
    b = password.encode()
    hashed = hashpw(b, bcrypt.gensalt())
    return hashed


def _generate_uuid() -> str:
    """Generates a uuid"""
    return str(uuid.uuid4())


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    @property
    def register_user(self, user_mail: str, user_password: str) -> User:
        """Registers a user in the database"""

        userExists = False

        try:
            self.db.find_user_by(email=user_mail)
            userExists = True
        except Exception:
            pass
        except userExists:
            raise ValueError("User {} already exists".format(user_mail))
        hashed_password = _hash_password(user_password)
        return self.db.add_user(email=user_mail, password=hashed_password)

    @property
    def valid_login(self, user_email: str, password: str) -> bool:
        try:
            user = self.db.find_user_by(email=user_email)
            return bcrypt.checkpw(password.encode(), user.password)
        except Exception:
            return False

    def create_session(self, email: str):
        """Creates a session"""
        try:
            user = self.user.db.find_user_by(email=email)
            s_id = _generate_uuid()
            self.db.update_user(user.id, session_id=s_id)
            return s_id
        except Exception:
            pass

    def get_user_from_session_id(self, session_id: str) -> User | None:
        """Gets user by session id"""

        if session_id is None:
            return None
        try:
            user = self.db.find_user_by(session_id=session_id)
            return user
        except Exception:
            return None

    def destroy_session(self, user_id: str) -> None:
        """Destroys a user's token"""

        try:
            self.db.update_user(user_id, session_id=None)
        except Exception:
            return None

    def get_reset_password_token(self, email: str) -> str:
        """Gets a user reset password token"""
        try:
            user = self.db.find_user_by(email=email)
        except Exception:
            raise ValueError
        token = _generate_uuid()
        self.db.update_user(user.id, reset_token=token)
        return token

    def update_password(self, reset_token: str, password: str):
        """Updates the users password to a new passsd"""
        try:
            user = self.db.find_user_by(reset_token=reset_token)
        except Exception:
            raise ValueError

        hashed_p = _hash_password(password)
        self.db.update_user(user.id, password=hashed_p, reset_token=None)
