# -*- coding: utf-8 -*-
"""
    flask-oauth2.core
    ~~~~~~~~~~~~~~~~~

    :copyright: (c) 2015 by Nicola Iarocci.
    :license: BSD, see LICENSE for more details.
"""
from flask.ext.pymongo import PyMongo
from flask_oauthlib.provider import OAuth2Provider
from redis import StrictRedis
from settings import REDIS_URL

mongo = PyMongo()
oauth = OAuth2Provider()
redis = StrictRedis.from_url(REDIS_URL)
