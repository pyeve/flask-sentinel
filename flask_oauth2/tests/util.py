import simplejson as json
import unittest

from flask_oauth2 import app
from flask_oauth2.core import mongo
from flask_oauth2.data import Storage


class TestBase(unittest.TestCase):

    def setUp(self):
        self.app = app.create_app('flask_oauth2.tests.test_settings')
        self.context = self.app.test_request_context('/')
        self.context.push()
        self.test_client = self.app.test_client()

        mongo.cx.drop_database(self.app.config['MONGO_DBNAME'])

        self.pw = 'pw'
        self.clientapp = Storage.generate_client()
        self.clientid = self.clientapp.client_id
        self.user = Storage.save_user("user", self.pw)
        self.username = self.user.username

        self.auth_endpoint = '/endpoint'
        self.token_endpoint = '/oauth/token'
        self.url = '%s?%s' % (
            self.token_endpoint,
            'client_id=%s&grant_type=password&username=%s&password=%s'
        )

    def tearDown(self):
        mongo.cx.drop_database(self.app.config['MONGO_DBNAME'])
        self.context.pop()

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
