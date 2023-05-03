#!/usr/bin/env python3
"""Basic auth"""


class BasicAuth:
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
