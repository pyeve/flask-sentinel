# -*- coding: utf-8 -*-
"""
    flask-sentinel.validator
    ~~~~~~~~~~~~~~~~~~~~~~~~

    :copyright: (c) 2015 by Nicola Iarocci.
    :license: BSD, see LICENSE for more details.
"""
from .data import Storage
from flask_oauthlib.provider import OAuth2RequestValidator
from flask_oauthlib.provider.oauth2 import log
from flask_oauthlib.utils import decode_base64
from oauthlib.common import to_unicode


class MyRequestValidator(OAuth2RequestValidator):
    """ Defines a custom OAuth2 Request Validator based on the Client, User
        and Token models.
    """
    def __init__(self):
        self._clientgetter = Storage.get_client
        self._usergetter = Storage.get_user
        self._tokengetter = Storage.get_token
        self._tokensetter = Storage.save_token

    def authenticate_client(self, request, *args, **kwargs):

        auth = request.headers.get('Authorization', None)
        if auth:
            try:
                _, s = auth.split(' ')
                client_id, client_secret = decode_base64(s).split(':')
                client_id = to_unicode(client_id, 'utf-8')
            except Exception as e:
                log.debug('Authenticate client failed with exception: %r', e)
                return False
        else:
            client_id = request.client_id

        client = self._clientgetter(client_id)
        if not client:
            log.debug('Authenticate client failed, client not found.')
            return False

        if client.client_type == 'public':
            return self.authenticate_client_id(client_id, request)
        else:
            return OAuth2RequestValidator.authenticate_client(
                self, request, *args, **kwargs)