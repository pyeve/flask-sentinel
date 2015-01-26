# -*- coding: utf-8 -*-
from flask import Blueprint, render_template, request

from core import oauth
from data import Storage

authapi = Blueprint('authapi', __name__)


@authapi.route('/oauth/token', methods=['POST'])
@oauth.token_handler
def access_token(*args, **kwargs):
    """ This endpoint is for exchanging/refreshing an access token.

    Returns a dictionary or None as the extra credentials for creating the
    token response.

    :param *args: Variable length argument list.
    :param **kwargs: Arbitrary keyword arguments.
    """
    return None


@authapi.route('/oauth/revoke', methods=['POST'])
@oauth.revoke_handler
def revoke_token():
    """ This endpoint allows a user to revoke their access token."""
    pass


@authapi.route('/', methods=['GET', 'POST'])
def management():
    """ This endpoint is for vieweing and adding users and clients. """
    if request.method == 'POST' and request.form['submit'] == 'Add User':
        Storage.save_user(request.form['username'], request.form['password'])
    if request.method == 'POST' and request.form['submit'] == 'Add Client':
        Storage.generate_client()
    return render_template('management.html', users=Storage.all_users(),
                           clients=Storage.all_clients())


@authapi.route('/endpoint')
@oauth.require_oauth()
def restricted_access():
    """ This is an example endpoint we are trying to protect. """
    return "Congratulations, you made it through and accessed the protected " \
        "resource!"
