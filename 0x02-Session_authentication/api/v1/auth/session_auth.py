#!/usr/bin/env python3
"""
session auth file
"""
from api.v1.auth.auth import Auth
import uuid


class SessionAuth(Auth):
    """
    session auth class
    """
    user_id_by_session_id = {}
    def create_session(self, user_id: str = None) -> str:
        """
        a method that creates a session id for a user_id
        """
        if user_id is None or type(user_id) is not str:
            return None
        session_id = str(uuid.uuid4())
        self.user_id_by_session_id[session_id] = user_id
        return session_id
