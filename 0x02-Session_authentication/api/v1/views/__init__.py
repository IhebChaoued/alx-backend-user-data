#!/usr/bin/env python3
from flask import Blueprint

app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')

from api.v1.views.session_auth import session_auth
app_views.register_blueprint(session_auth)
