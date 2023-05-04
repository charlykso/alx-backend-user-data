#!/usr/bin/env python3
"""Basic auth"""
import base64
import binascii
import flask
from typing import List, Tuple, TypeVar
from models.user import User
from .auth import Auth


class BasicAuth(Auth):
    """Basic auth class"""

    def extract_base64_authorization_header(self,
                                            authorization_header: str) -> str:
        """
        returns the Base64 part of the Authorization header
        for a Basic Authentication
        """
        if type(authorization_header) is not str or\
                authorization_header is None:
            return None
        if not authorization_header.startswith('Basic '):
            return None
        return authorization_header[6:]

    def decode_base64_authorization_header(
            self,
            base64_authorization_header: str) -> str:
        """
         returns the decoded value of a Base64 string
         base64_authorization_header
        """
        if type(base64_authorization_header) is not str or\
                base64_authorization_header is None:
            return None
        try:
            base64_bytes = base64_authorization_header.encode('ascii')
            decode_bytes = base64.b64decode(base64_bytes)
            decode_str = decode_bytes.decode('utf-8')
            return decode_str
        except (binascii.Error, UnicodeDecodeError):
            return None

    def extract_user_credentials(
        self,
            decoded_base64_authorization_header: str) -> Tuple[str, str]:
        """
        returns the user email and password from the Base64 decoded value
        """
        if type(decoded_base64_authorization_header) is not str or\
                decoded_base64_authorization_header is None:
            return None, None
        if ':' not in decoded_base64_authorization_header:
            return None, None
        user_credentials = decoded_base64_authorization_header.split(':')
        return user_credentials[0], user_credentials[1]

    def user_object_from_credentials(
        self,
            user_email: str, user_pwd: str) -> TypeVar('User'):
        """
        returns the User instance based on his email and password.
        """
        if type(user_email) is not str or user_email is None:
            return None
        if type(user_pwd) is not str or user_pwd is None:
            return None
        try:
            user = User.search({'email': user_email})
        except Exception:
            return None
        if len(user) <= 0:
            return None
        if user[0].is_valid_password(user_pwd):
            return user[0]
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """
        overloads Auth and retrieves the User instance for a request
        """
        authorization_header = self.authorization_header(request)
        if not authorization_header:
            return None

        encoded_credentials = self.extract_base64_authorization_header(
            authorization_header)
        if not encoded_credentials:
            return None

        decoded_credentials = self.decode_base64_authorization_header(
            encoded_credentials)
        if not decoded_credentials:
            return None

        email, password = self.extract_user_credentials(decoded_credentials)
        if not email or not password:
            return None

        user = self.user_object_from_credentials(email, password)
        return user
