"""
JSON Web Token auth for Tornado
Based on https://github.com/paulorodriguesxv/tornado-json-web-token-jwt
"""

import binascii
import os
import sys
import traceback
from functools import wraps

import jwt

jwt_options = {
    'verify_signature': True,
    'verify_exp': True,
    'verify_nbf': False,
    'verify_iat': True,
    'verify_aud': False
}


class UnauthorizedError(Exception):
    pass


class auth(object):

    AUTHORIZATION_HEADER = 'Authorization'
    AUTHORIZATION_METHOD = 'bearer'
    SECRET_KEY = binascii.hexlify(os.urandom(16)).decode('ascii')

    def __call__(self, handler_class):
        """
        Tornado JWT Auth Decorator
        """
        def wrap(f):
            @wraps(f)
            def prepare(this, *args, **kwargs):
                try:
                    self.require_auth(this)

                except UnauthorizedError as e:
                    this.unauthorized(str(e))

                except Exception:
                    this.server_error()
                    print(traceback.format_exc(), file=sys.stderr, flush=True)

                return f(this, transforms, *args, **kwargs)

            return prepare

        handler_class.prepare = wrap(handler_class.prepare)
        return handler_class

    def require_auth(self, handler):
        auth_header = handler.request.headers.get(auth.AUTHORIZATION_HEADER)

        if not auth_header:
            raise UnauthorizedError("Missing authorization")

        parts = auth_header.split()

        if not self.is_valid_header(parts):
            raise UnauthorizedError("Invalid header authorization")

        token = parts[1]
        try:
            jwt.decode(token, auth.SECRET_KEY, options=jwt_options)

        except jwt.InvalidTokenError as err:
            raise UnauthorizedError(err)

    def is_valid_header(self, parts):
        """
        Validate the header
        """
        if parts[0].lower() != auth.AUTHORIZATION_METHOD:
            return False
        elif len(parts) == 1:
            return False
        elif len(parts) > 2:
            return False

        return True
