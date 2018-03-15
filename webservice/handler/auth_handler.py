"""
JSON Web Token auth for Tornado
Based on https://github.com/paulorodriguesxv/tornado-json-web-token-jwt
"""
import datetime

import jwt
from webservice.handler.abstract_request_handler import AbstractRequestHandler
from webservice.util.auth import auth


class AuthHandler(AbstractRequestHandler):
    """
    Handle to auth method.
    This method aim to provide a new authorization token
    There is a fake payload (for tutorial purpose)
    """

    def initialize(self, app, webservice):
        super(AuthHandler, self).initialize(app, webservice)

    def prepare(self):
        """
        Encode a new token with JSON Web Token (PyJWT)
        """
        self.encoded = jwt.encode(
            {'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=7), 'data': 'asdasds'},
            auth.SECRET_KEY,
            algorithm='HS256'
        )

    def get(self, *args, **kwargs):
        """
        :return The generated token
        """
        self.write({'token': self.encoded.decode('ascii')})
