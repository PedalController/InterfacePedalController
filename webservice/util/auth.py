"""
JSON Web Token auth for Tornado
Based on https://github.com/paulorodriguesxv/tornado-json-web-token-jwt
"""

import binascii
import os
import sys
import traceback

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


class RequiresAuthMixing:
    """
    Uses this Mixing with AbstractRequestHandler
    """

    def auth(self):
        """
        :return bool: Is auth?
        """
        try:
            JWTAuth.require_auth(self)
            return True

        except UnauthorizedError as e:
            self.unauthorized(str(e))

        except Exception:
            self.server_error()
            print(traceback.format_exc(), file=sys.stderr, flush=True)

        return False

    def unauthorized(self, message):
        self.send(401, {"error": message})


class JWTAuth(object):

    AUTHORIZATION_HEADER = 'Authorization'
    AUTHORIZATION_METHOD = 'bearer'
    SECRET_KEY = binascii.hexlify(os.urandom(16)).decode('ascii')

    @staticmethod
    def require_auth(handler):
        auth_header = handler.request.headers.get(JWTAuth.AUTHORIZATION_HEADER)

        if not auth_header:
            raise UnauthorizedError("Missing authorization")

        parts = auth_header.split()

        if not JWTAuth.is_valid_header(parts):
            raise UnauthorizedError("Invalid header authorization")

        token = parts[1]
        try:
            jwt.decode(token, JWTAuth.SECRET_KEY, options=jwt_options)

        except jwt.InvalidTokenError as err:
            raise UnauthorizedError(err)

    @staticmethod
    def is_valid_header(parts):
        """
        Validate the header
        """
        if parts[0].lower() != JWTAuth.AUTHORIZATION_METHOD:
            return False
        elif len(parts) == 1:
            return False
        elif len(parts) > 2:
            return False

        return True
