#!/usr/bin/env python3
"""
auth class
"""
import re
from flask import request
from typing import List, TypeVar
import os


class Auth:
    """
    Implementing the Auth class
    """

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
        Check if path requires authentication
        Return bool value
        """
        if path is None:
            return True
        if excluded_paths is None or len(excluded_paths) == 0:
            return True
        for excluded_path in excluded_paths:
            if path.rstrip("/") == excluded_path.rstrip("/"):
                return False
            if excluded_path.endswith('*'):
                if path.startswith(excluded_path[:-1]):
                    return False
            elif path == excluded_path:
                return False
        return True

    def authorization_header(self, request=None) -> str:
        """
        validate all requests to secure the API
        returns string
        """
        if request is None:
            return None
        if 'Authorization' not in request.headers:
            return None
        return request.headers['Authorization']

    def current_user(self, request=None) -> TypeVar('User'):
        """
        returns None - request
        """
        return None

    def session_cookie(self, request=None):
        """
        returns a cookie value from a request
        """
        if request is None:
            return None
        return request.cookies.get(os.getenv(
            'SESSION_NAME', '_my_session_id'))
