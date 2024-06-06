#!/usr/bin/env python3
"""API entry point
"""
from os import getenv
from flask import Flask, jsonify, request, abort
from flask_cors import CORS
from api.v1.auth.auth import Auth
from api.v1.auth.session_auth import SessionAuth

from api.v1.views.index import *
from api.v1.views.users import *
from api.v1.views.session_auth import *

app = Flask(__name__)
CORS(app, resources={r"/api/v1/*": {"origins": "*"}})

auth = None
auth_type = getenv('AUTH_TYPE')

if auth_type == 'session_auth':
    auth = SessionAuth()
elif auth_type == 'basic_auth':
    from api.v1.auth.basic_auth import BasicAuth
    auth = BasicAuth()
else:
    auth = Auth()


@app.before_request
def before_request():
    """ Before request handler
    """
    excluded_paths = [
        '/api/v1/status/',
        '/api/v1/unauthorized/',
        '/api/v1/forbidden/',
        '/api/v1/auth_session/login/'
    ]
    if auth and auth.require_auth(request.path, excluded_paths):
        if not auth.authorization_header(
                request
                ) and not auth.session_cookie(request):
            abort(401)
        request.current_user = auth.current_user(request)


@app.errorhandler(401)
def unauthorized(error):
    """ Unauthorized handler
    """
    return jsonify({"error": "Unauthorized"}), 401


@app.errorhandler(403)
def forbidden(error):
    """ Forbidden handler
    """
    return jsonify({"error": "Forbidden"}), 403


@app.errorhandler(404)
def not_found(error):
    """ Not found handler
    """
    return jsonify({"error": "Not found"}), 404


if __name__ == "__main__":
    host = getenv("API_HOST", "0.0.0.0")
    port = getenv("API_PORT", "5000")
    app.run(host=host, port=port)
