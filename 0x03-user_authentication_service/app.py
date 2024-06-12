#!/usr/bin/env python3
"""
Basic Flask app
"""
from flask import Flask, jsonify, request, make_response, abort
from auth import Auth

app = Flask(__name__)
AUTH = Auth()


@app.route("/", methods=["GET"])
def welcome():
    """GET route that returns a welcome message."""
    return jsonify({"message": "Bienvenue"})


@app.route("/sessions", methods=["POST"])
def login():
    """POST route to log in a user."""
    email, password = request.form.get("email"), request.form.get("password")
    if not AUTH.valid_login(email, password):
        abort(401)
    session_id = AUTH.create_session(email)
    response = jsonify({"email": email, "message": "logged in"})
    response.set_cookie("session_id", session_id)
    return response


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
