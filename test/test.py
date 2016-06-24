import unittest

from test.rest_facade import RestFacade


class Test(unittest.TestCase):
    address = ''

    SUCCESS = 200
    CREATED = 201
    UPDATED = 200
    DELETED = 200

    ERROR = 400
    rest = RestFacade()
