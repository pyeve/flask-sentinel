# -*- coding: utf-8 -*-
"""
    flask-sentinel.models
    ~~~~~~~~~~~~~~~~~~~~~

    :copyright: (c) 2015 by Nicola Iarocci.
    :license: BSD, see LICENSE for more details.
"""


class BaseModel(object):
    def __init__(self, id=None):
        self._id = id

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, value):
        self._id = value


class User(BaseModel):
    """ User which will be querying resources from the API.
    """
    def __init__(self, id=None, username=None, hashpw=None):
        super(User, self).__init__(id)
        self._username = username
        self._hashpw = hashpw

    @property
    def username(self):
        return self._username

    @username.setter
    def username(self, value):
        self._username = value

    @property
    def hashpw(self):
        return self._hashpw

    @hashpw.setter
    def hashpw(self, value):
        self._hashpw = value


class Client(BaseModel):
    """ Client application through which user is authenticating.

    RFC 6749 Section 2 (http://tools.ietf.org/html/rfc6749#section-2)
    describes clients:

     +----------+
     | Resource |
     |  Owner   |
     |          |
     +----------+
          v
          |    Resource Owner
         (A) Password Credentials
          |
          v
     +---------+                                  +---------------+
     |         |>--(B)---- Resource Owner ------->|               |
     |         |         Password Credentials     | Authorization |
     | Client  |                                  |     Server    |
     |         |<--(C)---- Access Token ---------<|               |
     |         |    (w/ Optional Refresh Token)   |               |
     +---------+                                  +---------------+

    Redirection URIs are mandatory for clients. We skip this requirement
    as this example only allows the resource owner password credentials
    grant (described in Section 4.3). In this flow, the Authorization
    Server will not redirect the user as described in subsection 3.1.2
    (Redirection Endpoint).
    """
    def __init__(self, id=None, client_id=None, client_type=None):
        super(Client, self).__init__(id)
        self._client_id = client_id
        self._client_type = client_type

    @property
    def client_id(self):
        return self._client_id

    @client_id.setter
    def client_id(self, value):
        self._client_id = value

    @property
    def client_type(self):
        return self._client_type

    @client_type.setter
    def client_type(self, value):
        self._client_type = value

    @property
    def allowed_grant_types(self):
        """ Returns allowed grant types.

        Presently, only the password grant type is allowed.
        """
        return ['password']

    @property
    def default_scopes(self):
        """ Returns default scopes associated with the Client. """
        return []

    @property
    def default_redirect_uri(self):
        """ Return a blank default redirect URI since we are not implementing
            redirects.
        """
        return ''


class Token(BaseModel):
    """ Access or refresh token

        Because of our current grant flow, we are able to associate tokens
        with the users who are requesting them. This can be used to track usage
        and potential abuse. Only bearer tokens currently supported.
    """

    def __init__(self, id=None, client_id=None, user_id=None, user=None,
                 token_type=None, access_token=None, refresh_token=None,
                 expires=None, scopes=['']):
        super(Token, self).__init__(id)
        self._client_id = client_id
        self._user_id = user_id
        self._user = None
        self._token_type = token_type
        self._access_token = access_token
        self._refresh_token = refresh_token
        self._expires = expires
        self._scopes = scopes

    @property
    def client_id(self):
        return self._client_id

    @client_id.setter
    def client_id(self, value):
        self._client_id = value

    @property
    def user_id(self):
        return self._user_id

    @user_id.setter
    def user_id(self, value):
        self._user_id = value

    @property
    def user(self):
        return self._user

    @user.setter
    def user(self, value):
        self._user = value

    @property
    def token_type(self):
        return self._token_type

    @token_type.setter
    def token_type(self, value):
        self._token_type = value

    @property
    def access_token(self):
        return self._access_token

    @access_token.setter
    def access_token(self, value):
        self._access_token = value

    @property
    def refresh_token(self):
        return self._refresh_token

    @refresh_token.setter
    def refresh_token(self, value):
        self._refresh_token = value

    @property
    def expires(self):
        return self._expires.replace(tzinfo=None)

    @expires.setter
    def expires(self, value):
        self._expires = value

    @property
    def scopes(self):
        return self._scopes

    @scopes.setter
    def scopes(self, value):
        self._scopes = value
