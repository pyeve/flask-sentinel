# -*- coding: utf-8 -*-
"""
    flask_sentinel.tests
    ~~~~~~~~~~~~~~~~~~~~

    :copyright: (c) 2015 by Nicola Iarocci.
    :license: BSD, see LICENSE for more details.
"""
import json
import unittest
from flask import Flask
from flask.ext.sentinel import ResourceOwnerPasswordCredentials, oauth
from flask.ext.sentinel.core import mongo
from flask.ext.sentinel.data import Storage


def is_redis_available():
    try:
        from redis import Redis, ConnectionError
        try:
            Redis().flushdb()
        except ConnectionError:
            return False
    except ImportError:
        return False
    return True


class TestBase(unittest.TestCase):
    def setUp(self):
        self.app = Flask(__name__)
        self.dbkey = 'SENTINEL_MONGO_DBNAME'

        self.app.add_url_rule('/endpoint', view_func=restricted_access)
        self.app.config.update(self.settings())

        ResourceOwnerPasswordCredentials(self.app)

        self.context = self.app.test_request_context('/')
        self.context.push()
        self.test_client = self.app.test_client()

        mongo.cx.drop_database(self.app.config[self.dbkey])

        self.pw = 'pw'
        self.clientapp = Storage.generate_client()
        self.clientid = self.clientapp.client_id
        self.user = Storage.save_user("user", self.pw)
        self.username = self.user.username

        self.auth_endpoint = '/endpoint'
        self.token_endpoint = '/testauth/testtoken'
        self.man_endpoint = '/testauth/testman'
        self.url = '%s?%s' % (
            self.token_endpoint,
            'client_id=%s&grant_type=password&username=%s&password=%s'
        )

    def tearDown(self):
        mongo.cx.drop_database(self.app.config[self.dbkey])
        self.context.pop()

    def settings(self):
        return {
            self.dbkey: 'test_auth',
            'REDIS_URL': 'redis://localhost:6379/0',
            'OAUTH2_PROVIDER_TOKEN_EXPIRES_IN': 999,
            'SENTINEL_TOKEN_URL': '/testtoken',
            'SENTINEL_MANAGEMENT_URL': '/testman',
            'SENTINEL_ROUTE_PREFIX': '/testauth'
        }

    def get_token(self):
        query = self.url % (self.clientid, self.username, self.pw)
        r = self.test_client.post(query)
        self.assert200(r.status_code)
        return json.loads(r.get_data())

    def assert405(self, status_code):
        self.assertEqual(405, status_code)

    def assert400(self, status_code):
        self.assertEqual(400, status_code)

    def assert401(self, status_code):
        self.assertEqual(401, status_code)

    def assert200(self, status_code):
        self.assertEqual(200, status_code)


@oauth.require_oauth()
def restricted_access():
    """ This is an example endpoint we are trying to protect. """
    return "Congratulations, you made it through and accessed the protected " \
        "resource!"
