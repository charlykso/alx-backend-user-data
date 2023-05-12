#!/usr/bin/env python3
"""Auth file"""

import uuid
from bcrypt import hashpw, checkpw, gensalt
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import InvalidRequestError
from typing import Union


def _hash_password(password: str) -> bytes:
    """
    hash user password with bcrypt
    :param password: a string password to be hashed
    :return: bytes of the hashed password
    """
    return hashpw(password.encode('utf-8'), gensalt())


def _generate_uuid() -> str:
    """generate uuid
    :return: string representation of uuid
    """
    return str(uuid.uuid4())


class Auth:
    """Auth class to interact with the authentication database.
    """
    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """Registering user
        :param email: the email of the user
        :param password: the password of the user
        :return: the user object that was registered
        """
        try:
            self._db.find_user_by(email=email)
            raise ValueError('User {} already exists'.format(email))
        except NoResultFound:
            hashed_password = _hash_password(password)
            user = self._db.add_user(email=email,
                                     hashed_password=hashed_password)
            return user

    def valid_login(self, email: str, password: str) -> bool:
        """user login
        :param email: email of the user
        :param password: password of the user
        :return: true if the user matches and false if not
        """
        try:
            user = self._db.find_user_by(email=email)
        except (NoResultFound, InvalidRequestError):
            return False
        hashed_password = user.hashed_password.encode('utf-8')

        return checkpw(password.encode('utf-8'), hashed_password)

    def create_session(self, email: str) -> Union[str, None]:
        """create a sessionId and store it in the db
        :param email: email of the user for the session id
        :return: the sessionId created
        """
        try:
            found_user = self._db.find_user_by(email=email)
        except NoResultFound:
            return None
        session_id = _generate_uuid()
        self._db.update_user(user_id=found_user.id, session_id=session_id)
        return session_id

    def get_user_from_session_id(self, session_id: str) -> Union[User, None]:
        """
        get user using the session id
        :param session_id: the session_id of the user
        :return: coresponding user with the session_id
        """
        try:
            return self._db.find_user_by(session_id=session_id)
        except NoResultFound:
            return None
