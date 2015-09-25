# -*- coding: utf-8 -*-
"""
    flask-sentinel
    ~~~~~~~~~~~~~~

    :copyright: (c) 2015 by Nicola Iarocci.
    :license: BSD, see LICENSE for more details.
"""
from flask import Blueprint

from . import views
from .core import oauth, mongo, redis
from .utils import Config
from .validator import MyRequestValidator
from redis.connection import ConnectionPool


class ResourceOwnerPasswordCredentials(object):
    def __init__(self, app=None):
        self.app = app
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        config = Config(app)
        redis.connection_pool = ConnectionPool.from_url(
            config.value('REDIS_URL'))
        self.register_blueprint(app)

        if config.value('TOKEN_URL') is not False:
            app.add_url_rule(
                config.url_rule_for('TOKEN_URL'),
                view_func=views.access_token,
                methods=['POST']
            )

        if config.value('MANAGEMENT_URL') is not False:
            app.add_url_rule(
                config.url_rule_for('MANAGEMENT_URL'),
                view_func=views.management,
                methods=['POST', 'GET']
            )

        mongo.init_app(app, config_prefix='SENTINEL_MONGO')
        self.mongo = mongo
        oauth.init_app(app)
        oauth._validator = MyRequestValidator()

    def register_blueprint(self, app):
            module = Blueprint('flask-sentinel', __name__,
                               template_folder='templates')
            app.register_blueprint(module)
            return module
