#!/usr/bin/env python3
"""SessionDBAuth module"""
from api.v1.auth.session_exp_auth import SessionExpAuth
from models.user_session import UserSession
from datetime import datetime, timedelta
import uuid


class SessionDBAuth(SessionExpAuth):
    """SessionDBAuth class"""

    def create_session(self, user_id=None):
        """Create and store a UserSession"""
        if user_id is None:
            return None
        session_id = str(uuid.uuid4())
        user_session = UserSession(user_id=user_id, session_id=session_id)
        user_session.save()
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """Get User ID by session_id"""
        if session_id is None:
            return None
        try:
            sessions = UserSession.search({"session_id": session_id})
            if not sessions:
                return None
            session = sessions[0]
            if self.session_duration <= 0:
                return session.user_id
            created_at = session.created_at
            if created_at + timedelta(
                    seconds=self.session_duration) < datetime.now():
                return None
            return session.user_id
        except Exception:
            return None

    def destroy_session(self, request=None):
        """Destroy a UserSession by session_id"""
        if request is None:
            return False
        session_id = self.session_cookie(request)
        if session_id is None:
            return False
        try:
            sessions = UserSession.search({"session_id": session_id})
            if not sessions:
                return False
            session = sessions[0]
            session.remove()
            return True
        except Exception:
            return False
