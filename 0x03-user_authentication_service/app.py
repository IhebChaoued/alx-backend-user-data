#!/usr/bin/env python3
"""
Main file
"""
from flask import Flask, jsonify, request, abort, redirect
from auth import Auth

app = Flask(__name__)
auth = Auth()


@app.route('/', methods=['GET'])
def welcome() -> str:
    """Welcome route."""
    return jsonify({"message": "Bienvenue"})


@app.route('/sessions', methods=['DELETE'])
def logout() -> str:
    """Logout route."""
    session_id = request.cookies.get('session_id')
    if session_id:
        user = auth.get_user_from_session_id(session_id)
        if user:
            auth.destroy_session(user.id)
            return redirect('/')
    abort(403)


@app.route('/profile', methods=['GET'])
def profile() -> str:
    """Profile route."""
    session_id = request.cookies.get('session_id')
    if session_id:
        user = auth.get_user_from_session_id(session_id)
        if user:
            return jsonify({"email": user.email})
    abort(403)


@app.route('/reset_password', methods=['POST'])
def get_reset_password_token() -> str:
    """Reset password route."""
    email = request.form.get('email')
    try:
        reset_token = auth.get_reset_password_token(email)
        return jsonify({"email": email, "reset_token": reset_token}), 200
    except ValueError:
        abort(403)


@app.route('/reset_password', methods=['PUT'])
def update_password() -> str:
    """Update password route."""
    email = request.form.get('email')
    reset_token = request.form.get('reset_token')
    new_password = request.form.get('new_password')
    try:
        auth.update_password(reset_token, new_password)
        return jsonify({"email": email, "message": "Password updated"}), 200
    except ValueError:
        abort(403)


@app.route('/sessions', methods=['POST'])
def login() -> str:
    """Login route."""
    email = request.form.get('email')
    password = request.form.get('password')
    if auth.valid_login(email, password):
        session_id = auth.create_session(email)
        response = jsonify({"email": email, "message": "logged in"})
        response.set_cookie('session_id', session_id)
        return response, 200
    abort(401)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
