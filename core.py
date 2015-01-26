# -*- coding: utf-8 -*-
"""
    flask-oauth2.core
    ~~~~~~~~~~~~~~~~~

    :copyright: (c) 2015 by Nicola Iarocci.
    :license: BSD, see LICENSE for more details.
"""
from collections import namedtuple
from flask.ext.pymongo import PyMongo
from flask_oauthlib.provider import OAuth2Provider


# map collection _id (primary key) to class property.
idFieldsMap = namedtuple('idFields', 'cls, collection')
id = idFieldsMap(cls='id', collection='_id')

mongo = PyMongo()
oauth = OAuth2Provider()
