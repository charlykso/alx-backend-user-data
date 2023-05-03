#!/usr/bin/env python3
"""
auth class
"""
import re
from flask import request
from typing import List, TypeVar


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
        return True

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
