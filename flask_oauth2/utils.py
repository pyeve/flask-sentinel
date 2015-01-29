# -*- coding: utf-8 -*-
"""
    flask-oauth2.utils
    ~~~~~~~~~~~~~~~~~~

    :copyright: (c) 2015 by Nicola Iarocci.
    :license: BSD, see LICENSE for more details.
"""


class Config(object):
    def __init__(self, app):
        self.prefix = 'OAUTH2_PROVIDER'
        self.app = app

        # TODO we currently use the eventual database found in app.config,
        # which means that we're going to use the same database as the
        # main app. This might now be the desireded behaviour for some.
        # Consider the option of using a different database for oauth (which
        # might eventually coincide with main app's.)
        app.config.setdefault('MONGO_DBNAME', 'oauth')

        app.config.setdefault(self._key('ROUTE_PREFIX'), '/oauth')
        app.config.setdefault(self._key('TOKEN_URL'), '/token')
        app.config.setdefault(self._key('MANAGEMENT_URL'), '/management')
        app.config.setdefault(self._key('REDIS_URL'),
                              'redis://localhost:6379/0')

    def url_rule_for(self, _key):
        return '%s%s' % (self.value('ROUTE_PREFIX'), self.value(_key))

    def value(self, key):
        return self.app.config[self._key(key)]

    def _key(self, _key):
        return '%s_%s' % (self.prefix, _key)
