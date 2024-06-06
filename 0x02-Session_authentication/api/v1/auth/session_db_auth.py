#!/usr/bin/env python3
"""
SessionDBAuth module
"""
from datetime import datetime, timedelta
from api.v1.auth.session_exp_auth import SessionExpAuth
from models.user_session import UserSession


class SessionDBAuth(SessionExpAuth):
    """
    SessionDBAuth class that inherits from SessionExpAuth
    """
    def create_session(self, user_id=None):
        """
        Create a session ID for a given user_id and store it in the database
        """
        session_id = super().create_session(user_id)
        if session_id is None:
            return None

        user_session = UserSession(user_id=user_id, session_id=session_id)
        user_session.save()
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """
        Return a User ID based on a Session ID by querying the database
        """
        if session_id is None:
            return None

        UserSession.load_from_file()
        sessions = UserSession.search({"session_id": session_id})
        if not sessions:
            return None

        user_session = sessions[0]
        if self.session_duration <= 0:
            return user_session.user_id

        created_at = user_session.created_at
        if created_at is None:
            return None

        if created_at + timedelta(
                seconds=self.session_duration
                ) < datetime.now():
            return None

        return user_session.user_id

    def destroy_session(self, request=None):
        """
        Destroy the UserSession based on the Session ID from the request cookie
        """
        if request is None:
            return False

        session_id = self.session_cookie(request)
        if session_id is None:
            return False

        UserSession.load_from_file()
        sessions = UserSession.search({"session_id": session_id})
        if not sessions:
            return False

        user_session = sessions[0]
        user_session.remove()
        return True
