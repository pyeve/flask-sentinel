# -*- coding: utf-8 -*-
"""
    flask_sentinel.basicauth
    ~~~~~~~~~~~~~~~~~~~~~~~~

    :copyright: (c) 2015 by Nicola Iarocci.
    :license: BSD, see LICENSE for more details.
"""
from flask import request, Response, current_app
from functools import wraps


def check_auth(username, password, expected_user, expected_pw):
        """This function is called to check if a username /
            password combination is valid.
        """
        return username == expected_user and password == expected_pw


def authenticate():
    """Sends a 401 response that enables basic auth"""
    return Response('Could not verify your access level for that URL.\n'
                    'You have to login with proper credentials', 401,
                    {'WWW-Authenticate': 'Basic realm="Login Required"'}
                    )


def requires_basicauth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        user = current_app.config.get('SENTINEL_MANAGEMENT_USERNAME')
        pw = current_app.config.get('SENTINEL_MANAGEMENT_PASSWORD')
        auth = request.authorization
        if user and pw:
            if not auth or \
                    not check_auth(auth.username, auth.password, user, pw):
                return authenticate()
        return f(*args, **kwargs)
    return decorated
