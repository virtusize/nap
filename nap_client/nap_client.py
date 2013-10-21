# -*- coding: utf-8 -*-

import urllib
import requests
from inflection import dasherize, underscore, pluralize
from flask.json import JSONDecoder, JSONEncoder
from nap.model import Model


class NapClient(object):

    def __init__(self, app, api, token=None):
        self.app = app
        self.api = api
        self.c = app.test_client()
        self.token = token

    def index(self, resource_name):
        return self._call(resource_name)

    def get(self, resource_name, id):
        return self._call(resource_name, id)

    def post(self, resource_name, data):
        return self._call(resource_name, data=data, method='POST')

    def put(self, resource_name, id, data):
        return self._call(resource_name, id, data=data, method='PUT')

    def patch(self, resource_name, id, data):
        return self._call(resource_name, id, data=data, method='PATCH')

    def delete(self, resource_name, id):
        return self._call(resource_name, id, method='DELETE')

    def query(self, resource_name, query):
        return self._call(resource_name, path='query?%s' % urllib.urlencode(query))

    def _modelize(self, data):
        if isinstance(data, list):
            return [Model(**item) for item in data]
        return Model(**data)

    def _handle_response(self, data, status_code):
        data = JSONDecoder().decode(data)
        if status_code < 500:
            return self._modelize(data)
        elif status_code >= 500:
            raise Exception('Status: %s' % data['status_code'] + ' - Message: %s' % data['message'])

    def _endpoint_prefix(self, resource_name):
        return dasherize(underscore(pluralize(resource_name)))

    def _headers(self, headers={'content-type': 'application/json'}):
        if self.token:
            headers['Authorization'] = self.token
        return headers

    def _url_for(self, resource_name, path=''):
        url = self.api.url_prefix + '/' + self._endpoint_prefix(resource_name) + '/' + str(path)

        return url

    def _call(self, resource_name, path='', method='GET', data=None):
        url = self._url_for(resource_name, path)

        if data:
            response = getattr(self.c, method.lower())(url, data=JSONEncoder().encode(data), headers=self._headers())
        else:
            response = getattr(self.c, method.lower())(url, headers=self._headers())

        return self._handle_response(response.data, response.status_code)


class HttpNapClient(NapClient):

    def __init__(self, base_url, token=None):
        self.base_url = base_url
        self.timeout = 10
        self.token = token

    def _url_for(self, resource_name, path=''):
        url = self.base_url + self._endpoint_prefix(resource_name) + '/' + str(path)

        return url

    def _call(self, resource_name, path='', method='GET', data=None):
        url = self._url_for(resource_name, path)

        method = getattr(requests, method.lower())
        if data:
            response = method(url, data=JSONEncoder().encode(data), headers=self._headers(), timeout=self.timeout)
        else:
            response = method(url, headers=self._headers(), timeout=self.timeout)

        return self._handle_response(response.content, response.status_code)
