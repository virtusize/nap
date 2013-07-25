# -*- coding: utf-8 -*-

import requests
from rest_app import app


class Resource(object):
    """A REST Resource"""

    name = "Resource"

    def __init__(self, base_uri):
        self.base_uri = base_uri

    def all(self):
        app.logger.debug('index: ' + self.base_uri)
        r = requests.get(self.base_uri)
        return r.json()

    def get(self, id):
        app.logger.debug('show: ' + self.base_uri + '/' + str(id))
        r = requests.get(self.base_uri + '/' + str(id))
        return r.json()


class Todos(Resource):
    def __init__(self, base):
        self.base_uri = base + '/todos'
