# -*- coding: utf-8 -*-
"""
    flask-oauth2.app
    ~~~~~~~~~~~~~~~~

    :copyright: (c) 2015 by Nicola Iarocci.
    :license: BSD, see LICENSE for more details.
"""
import logging
from flask import Flask

from core import oauth, mongo
from validator import MyRequestValidator
from views import authapi


def create_app(settings='settings', settings_override=None):
    """ Method for creating and initializing application.

        :param settings_override: Dictionary of settings to override.
    """
    app = Flask(__name__)

    # Update configuration.
    app.config.from_object(settings)
    app.config.from_pyfile('settings.cfg', silent=True)
    app.config.from_object(settings_override)

    # Initialize extensions on the application.
    mongo.init_app(app)
    oauth.init_app(app)
    oauth._validator = MyRequestValidator()

    # Register views on the application.
    app.register_blueprint(authapi)

    return app


if __name__ == '__main__':

    # Enable Flask-OAuthlib logging for this application.
    logger = logging.getLogger('flask_oauthlib')
    logger.addHandler(logging.StreamHandler())
    logger.setLevel(logging.DEBUG)

    # Create app and SQL schemas in database, then run the application.
    app = create_app()
    app.run(ssl_context='adhoc')
