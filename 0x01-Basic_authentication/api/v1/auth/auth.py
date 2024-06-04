#!/usr/bin/env python3
"""
Auth module for the API
"""
from flask import request
from typing import List, TypeVar


class Auth:
    """ Auth class to manage API authentication
    """

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """ Checks if authentication is required
        """
        return False

    def authorization_header(self, request=None) -> str:
        """ Returns the authorization header
        """
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """ Returns the current user
        """
        return None
