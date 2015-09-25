# -*- coding: utf-8 -*-
"""
    flask-sentinel.tests.tests
    ~~~~~~~~~~~~~~~~~~~~~~~~~~

    :copyright: (c) 2015 by Nicola Iarocci.
    :license: BSD, see LICENSE for more details.
"""
import unittest

from .base import TestBase, is_redis_available
from ..core import mongo, redis
from ..data import Storage
from ..models import Client, User


class TestTokenEndpoint(TestBase):
    def test_methods_not_allowed(self):
        r = self.test_client.get(self.token_endpoint)
        self.assert405(r.status_code)

        r = self.test_client.put(self.token_endpoint)
        self.assert405(r.status_code)

        r = self.test_client.delete(self.token_endpoint)
        self.assert405(r.status_code)

        r = self.test_client.patch(self.token_endpoint)
        self.assert405(r.status_code)

    def test_invalid_token_request(self):
        r = self.test_client.post(self.token_endpoint)
        self.assert400(r.status_code)

        query = self.url % ('notreally', self.username, self.pw)
        r = self.test_client.post(query)
        self.assert401(r.status_code)

        query = self.url % (self.clientid, 'notreally', self.pw)
        r = self.test_client.post(query)
        self.assert401(r.status_code)

        query = self.url % (self.clientid, self.username, 'notreally')
        r = self.test_client.post(query)
        self.assert401(r.status_code)

    @unittest.skipIf(is_redis_available() is False, "redis server unavailable")
    def test_valid_token_request(self):
        son = self.get_token()
        self.assertTrue('access_token' in son)
        self.assertTrue('token_type' in son)
        self.assertTrue('refresh_token' in son)
        self.assertTrue('scope' in son)
        self.assertEqual('Bearer', son['token_type'])
        self.assertEqual('', son['scope'])

        # Test that token has been stored in redis
        token_key = son['access_token']
        token = redis.get(token_key)
        # Test that key value matches user id.
        self.assertEqual(token, str(self.user.id))
        # Test that TTL has been set to custom value.
        ttl = redis.ttl(token_key)
        self.assertEqual(ttl, 999)


class TestAuthEndpoint(TestBase):
    def test_no_auth(self):
        r = self.test_client.get(self.auth_endpoint)
        self.assert401(r.status_code)

    def test_invalid_auth(self):
        headers = [('Authorization', 'Bearer DontThinkSo')]
        r = self.test_client.get(self.auth_endpoint, headers=headers)
        self.assert401(r.status_code)

        headers = [('Authorization', 'Basic DontThinkSo')]
        r = self.test_client.get(self.auth_endpoint, headers=headers)
        self.assert401(r.status_code)

    @unittest.skipIf(is_redis_available() is False, "redis server unavailable")
    def test_valid_auth(self):
        son = self.get_token()
        token = son['access_token']
        headers = [('Authorization', 'Bearer %s' % token)]
        r = self.test_client.get(self.auth_endpoint, headers=headers)
        self.assert200(r.status_code)


class TestManagementEndpoint(TestBase):
    def test_man_endpoint(self):
        # management endpoint is accessible with no auth
        r = self.test_client.get(self.man_endpoint)
        self.assert200(r.status_code)

        self.app.config['SENTINEL_MANAGEMENT_USERNAME'] = 'user'
        self.app.config['SENTINEL_MANAGEMENT_PASSWORD'] = 'pw'

        # inaccessible with no auth
        r = self.test_client.get(self.man_endpoint)
        self.assert401(r.status_code)

        # inaccessible with bad auth
        headers = [('Authorization', 'Basic %s' % 'DontThinkSo')]
        r = self.test_client.get(self.man_endpoint, headers=headers)
        self.assert401(r.status_code)

        # green light
        headers = [('Authorization', 'Basic %s' % 'dXNlcjpwdw==')]
        r = self.test_client.get(self.man_endpoint, headers=headers)
        self.assert200(r.status_code)


class TestStorage(TestBase):
    def test_get_client(self):
        client = Storage.get_client('notreally')
        self.assertIsNone(client)

        client = Storage.get_client(self.clientid)
        self.assertIsInstance(client, Client)
        self.assertEqual(client.client_id, self.clientid)
        self.assertEqual(client.client_type, 'public')
        self.assertEqual(client.allowed_grant_types, ['password'])
        self.assertEqual(client.default_scopes, [])
        self.assertEqual(client.default_redirect_uri, '')

    def test_generate_client(self):
        client = Storage.generate_client()
        self.assertEqual(mongo.db.clients.count(), 2)

        compare = Storage.get_client(client.client_id)
        self.assertEqual(client.client_id, compare.client_id)

    def test_all_clients(self):
        client = Storage.generate_client()
        clients = Storage.all_clients()

        self.assertIsInstance(clients, list)
        self.assertEqual(len(clients), 2)
        self.assertEqual(clients[0].client_id, self.clientid)
        self.assertEqual(clients[1].client_id, client.client_id)

    def test_get_user(self):
        user = Storage.get_user('notreally', 'notreally')
        self.assertIsNone(user)

        user = Storage.get_user(self.username, self.pw)
        self.assertIsInstance(user, User)
        self.assertEqual(user.username, self.username)
        self.assertEqual(user.hashpw, self.user.hashpw)

    def test_save_user(self):
        user = Storage.save_user('test', 'testpw')
        self.assertEqual(mongo.db.users.count(), 2)

        compare = Storage.get_user('test', 'testpw')
        self.assertEqual(compare.username, user.username)
        self.assertEqual(compare.hashpw, user.hashpw)

    def test_all_users(self):
        user = Storage.save_user('test', 'testpw')
        users = Storage.all_users()

        self.assertIsInstance(users, list)
        self.assertEqual(len(users), 2)
        self.assertEqual(users[0].username, self.user.username)
        self.assertEqual(users[0].hashpw, self.user.hashpw)
        self.assertEqual(users[1].username, user.username)
        self.assertEqual(users[1].hashpw, user.hashpw)
