# -*- coding: utf-8 -*-
from flask_oauthlib.provider import OAuth2RequestValidator

from data import Storage


class MyRequestValidator(OAuth2RequestValidator):
    """ Defines a custom OAuth2 Request Validator based on the Client, User
        and Token models.
    """
    def __init__(self):
        self._clientgetter = Storage.get_client
        self._usergetter = Storage.get_user
        self._tokengetter = Storage.get_token
        self._tokensetter = Storage.save_token
