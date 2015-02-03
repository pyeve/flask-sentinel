Flask-OAuth2
============
OAuth2 Provider currently supporting the Resource Owner Password Credentials
Grant as described in Section 1.3.3 of `RFC 6749`_.

Powered by Flask, Redis and MongoDB.

Deployment
----------
Clone this repository and install all dependencies:

.. code-block:: console

    $ pip install -r requirements.txt

Once v0.0.1 is released (which is not the case yet) you will be able to install
as usual:

.. code-block:: console

    $ pip install flask-oauth2

Usage
-----
Once the extension and its dependencies are installed, you can use it like any
other Flask extension:

.. code-block:: python

    from flask import Flask
    from flask_oauth2 import ResourceOwnerPasswordCredentials, oauth


    app = Flask(__name__)
    ResourceOwnerPasswordCredentials(app)


    @app.route('/endpoint')
    @oauth.require_oauth()
    def restricted_access():
        return "You made it through and accessed the protected resource!"

    if __name__ == '__main__':
        app.run(ssl_context='adhoc')

User and Client Management
--------------------------
You can create users and clients through the default management interface
available at ``https://localhost:5000/oauth/management``.

.. image:: static/console.png

Testing
-------
After creating a user and client, you may use ``curl`` to test the application.

Generating a Bearer Token
~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: console

    $ curl -k -X POST -d "client_id=9qFbZD4udTzFVYo0u5UzkZX9iuzbdcJDRAquTfRk&grant_type=password&username=jonas&password=pass" https://localhost:5000/oauth/token
    {"access_token": "NYODXSR8KalTPnWUib47t5E8Pi8mo4", "token_type": "Bearer", "refresh_token": "s6L6OPL2bnKSRSbgQM3g0wbFkJB4ML", "scope": ""}

Accessing a Protected Resource Using Retrieved Bearer Token
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: console

    $ curl -k -H "Authorization: Bearer NYODXSR8KalTPnWUib47t5E8Pi8mo4" https://localhost:5000/endpoint
    You made it through and accessed the protected resource!

Configuration
-------------
Configuration works like any other `Flask configuration`_. Here are
the built-in defaults:

.. tabularcolumns:: |p{6.5cm}|p{8.5cm}|

======================================= ======================================
``OAUTH2_PROVIDER_ROUTE_PREFIX``        Default prefix for OAuth endpoints. 
                                        Defaults to ``/oauth``. Prepends both
                                        token and management urls.

``OAUTH2_PROVIDER_TOKEN_URL``           Url for token creation endpoint. 
                                        Defaults to ``/token``, so the 
                                        complete url is ``/oauth/token``. 

``OAUTH2_PROVIDER_MANAGEMENT_URL``      Url for management endpoint. Defaults 
                                        to ``/management``, so the complete 
                                        url is ``/oauth/management``. 

``OAUTH2_PROVIDER_TOKEN_EXPIRES_IN``    Default Bearer token expires time, 
                                        default is ``3600``.

``OAUTH2_PROVIDER_REDIS_URL``           Url for the redis server. Defaults to 
                                        ``redis://localhost:6379/0``. 

``OAUTH2_PROVIDER_ERROR_URI``           The error page when there is an error, 
                                        default value is ``/oauth/errors``. 

``OAUTH2_PROVIDER_ERROR_ENDPOINT``      You can also configure the error page 
                                        uri with an endpoint name. 

``OAUTH2_PROVIDER_MONGO_DBNAME``        Mongo database name. Defaults to 
                                        ``oauth``. 
======================================= ======================================

Other standard PyMongo settings such as ``MONGO_HOST``, ``MONGO_PORT``,
``MONGO_URI`` are also supported; just prefix them with ``OAUTH2_PROVIDER_`` as
seen above.

When a token is created it is added to both the database and the Redis cache.
In Redis, ``key`` is the access token itself while ``value`` is the id of the
user who requested the token. This allows for fast token
authentication/verification bypassing the database lookup. This tecnique can be
used, for example, when integrating ``flask-oauth`` with `Eve`_ powered REST
API instances.

Using Flask-OAuth2 with Eve
---------------------------
See the `Eve-OAuth2`_ example project.

Security
--------
SSL/TLS
~~~~~~~
When working with OAuth 2.0, all communications must be encrypted with SSL/TLS.
This example uses auto-generated SSL certificates, however in a production
environment you should use a more formal, widely trusted certificate associated
with your domain. In addition, requests should be handled by something like
NGINX and proxied to the authentication service.

*Note: Add `-k` to your `curl` arguments if you are working with an untrusted
development server running under SSL/TLS.*

Password Hashing
~~~~~~~~~~~~~~~~
Bcrypt and a randomly generated salt are used to hash each user password before
it is added to the database. You should never store passwords in plain text! 

License
-------
Flask-OAuth2 is a `Nicola Iarocci`_ and `Gestionali Amica`_ open source project
distributed under the `BSD license`_.

Acknowledgement
---------------
This work is based on the `yoloAPI`_ project by `Josh Brandoff`_ and `Jonas Brunsgaard`_.

.. _`RFC 6749`: http://tools.ietf.org/html/rfc6749#section-1.3.3
.. _`yoloAPI`: https://github.com/brunsgaard/yoloAPI
.. _`Josh Brandoff`: https://github.com/EmergentBehavior
.. _`Jonas Brunsgaard`: https://github.com/brunsgaard
.. _`Nicola Iarocci`: http://nicolaiarocci.com
.. _`Gestionali Amica`: http://gestionaleamica.com
.. _`BSD license`: https://github.com/nicolaiarocci/flask-oauth2/blob/master/LICENSE
.. _`Eve-OAuth2`: https://github.com/nicolaiarocci/eve-oauth2
.. _`Eve`: http://python-eve.org
.. _`Flask configuration`: http://flask.pocoo.org/docs/0.10/config/
