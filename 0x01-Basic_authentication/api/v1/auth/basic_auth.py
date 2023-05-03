#!/usr/bin/env python3
"""Basic auth"""
import base64
import binascii


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
