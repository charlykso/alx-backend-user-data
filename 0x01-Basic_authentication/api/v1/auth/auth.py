#!/usr/bin/env python3
"""
auth class
"""
from flask import request
from typing import List, TypeVar


class Auth:
    """
    Implementing the Auth class
    """

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
        Return bool value
        """
        return False

    def authorization_header(self, request=None) -> str:
        """
        returns None - request
        """
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """
        returns None - request
        """
        return None
