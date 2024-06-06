#!/usr/bin/env python3
"""
Flask view for Session Authentication
"""
from flask import Blueprint, request, jsonify, abort
from models.user import User
from api.v1.app import auth
import os

session_auth = Blueprint(
        'session_auth', __name__, url_prefix='/api/v1/auth_session'
        )


@session_auth.route('/login', methods=['POST'], strict_slashes=False)
def login():
    """ POST /api/v1/auth_session/login
    Handles session authentication
    """
    email = request.form.get('email')
    password = request.form.get('password')

    if email is None or email == "":
        return jsonify({"error": "email missing"}), 400
    if password is None or password == "":
        return jsonify({"error": "password missing"}), 400

    try:
        user = User.search({"email": email})
    except Exception:
        user = None

    if not user:
        return jsonify({"error": "no user found for this email"}), 404

    user = user[0]

    if not user.is_valid_password(password):
        return jsonify({"error": "wrong password"}), 401

    session_id = auth.create_session(user.id)
    user_json = user.to_json()
    response = jsonify(user_json)
    session_name = os.getenv('SESSION_NAME', '_my_session_id')
    response.set_cookie(session_name, session_id)

    return response
