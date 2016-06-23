import unittest
import requests

import json


class Test(unittest.TestCase):
    address = ''

    SUCCESS = 200
    CREATED = 201
    UPDATED = 200
    DELETED = 200

    ERROR = 400

    def get(self, url):
        print('[GET]', self.address + url)
        return requests.get(self.address + url)

    def post(self, url, data):
        print('[POST]', self.address + url)
        return requests.post(
            self.address + url,
            data=json.dumps(data),
            headers={'content-type': 'application/json'}
        )

    def put(self, url, data):
        print('[PUT]', self.address + url)
        return requests.put(
            self.address + url,
            data=json.dumps(data),
            headers={'content-type': 'application/json'}
        )

    def delete(self, url):
        print('[DELETE]', self.address + url)
        return requests.delete(self.address + url)
