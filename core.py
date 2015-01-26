# -*- coding: utf-8 -*-

"""
    flask-oauth2.core
    ~~~~~~~~~~~~~~~~~

    This module holds Flask itself, flask extensions and oauth provider.
"""
from collections import namedtuple
from flask.ext.pymongo import PyMongo
from flask_oauthlib.provider import OAuth2Provider


# map collection _id (primary key) to class property.
idFieldsMap = namedtuple('idFields', 'cls, collection')
id = idFieldsMap(cls='id', collection='_id')

mongo = PyMongo()
oauth = OAuth2Provider()
