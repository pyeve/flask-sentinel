# Flask-OAuth2
OAuth2 Provider for the Resource Owner Password Credentials Grant scheme, as
described in [RFC 6749 (Section 1.3.3)][1].

Powered by Flask, Redis and MongoDB.

## Deployment
Clone this repository and install all dependencies:

```bash
$ pip install -r requirements.txt
```

Once v0.0.1 is released (which is not the case yet) you will be able to install
as usual:

```bash
$ pip install flask-oauth2
```

## Usage
Once the extension and its dependencies are installed, you can use it like any
other Flask extension:

```python

from flask import Flask
from flask_oauth2 import ResourceOwnerPasswordCredentials, oauth


app = Flask(__name__)
ResourceOwnerPasswordCredentials(app)


@app.route('/endpoint')
@oauth.require_oauth()
def restricted_access():
    """ This is an example endpoint we are trying to protect. """
    return "Congratulations, you made it through and accessed the protected " \
        "resource!"

if __name__ == '__main__':
    app.run(ssl_context='adhoc')
```

Ok the class name kind of sucks. Will try to come up with something more
concise ;-)

## User and Client Management
You can create users and clients through the default management interface
available at [https://localhost:5000/oauth/management][8].

![API Management Console][console]

## Testing
After creating a user and client, you may use `curl` to test the application.

### Generating a Bearer Token
```bash
$ curl -k -X POST -d "client_id=9qFbZD4udTzFVYo0u5UzkZX9iuzbdcJDRAquTfRk&grant_type=password&username=jonas&password=pass" https://localhost:5000/oauth/token
{"access_token": "NYODXSR8KalTPnWUib47t5E8Pi8mo4", "token_type": "Bearer", "refresh_token": "s6L6OPL2bnKSRSbgQM3g0wbFkJB4ML", "scope": ""}
```

### Accessing a Protected Resource Using Retrieved Bearer Token
```bash
$ curl -k -H "Authorization: Bearer NYODXSR8KalTPnWUib47t5E8Pi8mo4" https://localhost:5000/endpoint
Congraulations, you made it through and accessed the protected resource!
```

## Configuration

## Security
### SSL/TLS
When working with OAuth 2.0, all communications must be encrypted with SSL/TLS.
This example uses auto-generated SSL certificates, however in a production
environment you should use a more formal, widely trusted certificate associated
with your domain. In addition, requests should be handled by something like
NGINX and proxied to the authentication service.

*Note: Add `-k` to your `curl` arguments if you are working with an untrusted
development server running under SSL/TLS.*

### Password Hashing
Bcrypt and a randomly generated salt are used to hash each user password before
it is added to the database. You should never store passwords in plain text! 

## License
Flask-OAuth2 is a [Nicola Iarocci][5] and [Gestionali Amica][6] open source project
distributed under the [BSD license][7].

## Acknowledgement
This work is based on the [yoloAPI][2] project by [Josh Brandoff][3] and [Jonas Brunsgaard][4].

[1]: http://tools.ietf.org/html/rfc6749#section-1.3.3
[2]: https://github.com/brunsgaard/yoloAPI
[3]: https://github.com/EmergentBehavior
[4]: https://github.com/brunsgaard
[5]: http://nicolaiarocci.com
[6]: http://gestionaleamica.com
[7]: https://github.com/nicolaiarocci/flask-oauth2/blob/master/LICENSE
[8]: https://localhost:5000/oauth/management
[console]: static/console.png
