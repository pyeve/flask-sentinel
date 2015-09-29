# -*- coding: utf-8 -*-
"""
    flask-sentinel.views
    ~~~~~~~~~~~~~~~~~~~~

    :copyright: (c) 2015 by Nicola Iarocci.
    :license: BSD, see LICENSE for more details.
"""
from flask import render_template, request

from .core import oauth
from .data import Storage
from .basicauth import requires_basicauth


@oauth.token_handler
def access_token(*args, **kwargs):
    """ This endpoint is for exchanging/refreshing an access token.

    Returns a dictionary or None as the extra credentials for creating the
    token response.

    :param *args: Variable length argument list.
    :param **kwargs: Arbitrary keyword arguments.
    """
    return None


@requires_basicauth
def management():
    """ This endpoint is for vieweing and adding users and clients. """
    if request.method == 'POST' and request.form['submit'] == 'Add User':
        Storage.save_user(request.form['username'], request.form['password'])
    if request.method == 'POST' and request.form['submit'] == 'Add Client':
        Storage.generate_client()
    return render_template('management.html', users=Storage.all_users(),
                           clients=Storage.all_clients())
