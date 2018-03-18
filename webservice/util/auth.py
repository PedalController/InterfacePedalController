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

    def auth(self, ignore_methods=('OPTIONS',)):
        """
        :param tuple ignore_methods: All methods that are be ignored
        :return bool: Is auth?
        """
        try:
            JWTAuth.require_auth(self, ignore_methods)
            return True

        except UnauthorizedError as e:
            self.unauthorized(str(e))

        except Exception:
            self.server_error()
            print(traceback.format_exc(), file=sys.stderr, flush=True)

        return False

    def unauthorized(self, message):
        self.send(401, {"error": message})


def generate_random_string(size):
    """
    Generate a random string with size specified
    Like python 3.6 secrets

    :param int size: Size of the random string that will be generated
    """
    return binascii.hexlify(os.urandom(size)).decode('ascii')


class JWTAuth(object):

    AUTHORIZATION_HEADER = 'Authorization'
    AUTHORIZATION_METHOD = 'bearer'
    SECRET_KEY = generate_random_string(16)

    @staticmethod
    def auth_token(token):
        try:
            jwt.decode(token, JWTAuth.SECRET_KEY, options=jwt_options)

        except jwt.InvalidTokenError as err:
            raise UnauthorizedError(err)

    @staticmethod
    def require_auth(handler, ignore_methods):
        """
        :param tornado.web.RequestHandler handler:
        :param tuple ignore_methods: All methods that are be ignored
        :return:
        """
        if handler.request.method in ignore_methods:
            return True

        header = handler.request.headers.get(JWTAuth.AUTHORIZATION_HEADER)

        if not header:
            raise UnauthorizedError("Missing authorization")

        auth_header = JWTAuth.extract_header(header)
        if auth_header['method'].lower() != JWTAuth.AUTHORIZATION_METHOD:
            raise JWTAuth._invalid_header_authorization()

        JWTAuth.auth_token(auth_header['token'])

    @staticmethod
    def extract_header(header):
        try:
            parts = header.split()

            return {
                'method': parts[0].lower(),
                'token': parts[1]
            }

        except Exception:
            raise JWTAuth._invalid_header_authorization()

    @staticmethod
    def _invalid_header_authorization():
        return UnauthorizedError("Invalid header authorization."
                                 " The Authorization header not match with the standard"
                                 " `Authorization: bearer <token>`")

    @staticmethod
    def extract_token(request):
        """
        Try extract token from request.
        It not validate if is valid or if the header has a correct format
        :param HTTPRequest request:
        """
        return JWTAuth.extract_header(request.headers.get(JWTAuth.AUTHORIZATION_HEADER))['token']
