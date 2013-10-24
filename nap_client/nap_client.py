# -*- coding: utf-8 -*-

import urllib
import requests
from inflection import dasherize, underscore, pluralize
from flask_nap.view_filters import UnderscoreFilter, CamelizeFilter
from nap.model import Model
from nap.util import encode_json, decode_json


class NapClient(object):
    input_filter = UnderscoreFilter()
    output_filter = CamelizeFilter()

    def __init__(self, app, api, token=None):
        self.app = app
        self.api = api
        self.c = app.test_client()
        self.token = token

    def index(self, resource_name):
        return self.call(resource_name)

    def get(self, resource_name, id):
        return self.call(resource_name, id)

    def post(self, resource_name, data):
        return self.call(resource_name, data=data, method='POST')

    def put(self, resource_name, id, data):
        return self.call(resource_name, id, data=data, method='PUT')

    def patch(self, resource_name, id, data):
        return self.call(resource_name, id, data=data, method='PATCH')

    def delete(self, resource_name, id):
        return self.call(resource_name, id, method='DELETE')

    def query(self, resource_name, query):
        return self.call(resource_name, path='query?%s' % urllib.urlencode(query))

    def save(self, model_or_list):
        if isinstance(model_or_list, list):
            res = []

            for model in model_or_list:
                res.append(self._create_or_update(model))

            return res
        else:
            return self._create_or_update(model_or_list)

    def call(self, resource_name, path='', method='GET', data=None):
        url = self._url_for(resource_name, path)

        if data:
            response = getattr(self.c, method.lower())(url, data=self._serialize(data), headers=self._headers())
        else:
            response = getattr(self.c, method.lower())(url, headers=self._headers())

        return self._handle_response(resource_name, response.data, response.status_code)

    def _create_or_update(self, model):
        if hasattr(model, 'id'):
            return self.put(model._resource, model.id, data=model.__getstate__())
        else:
            return self.post(model._resource, data=model.__getstate__())

    def _modelize(self, resource_name, data):
        if isinstance(data, list):
            for item in data:
                item['_resource'] = resource_name

            return [Model(**item) for item in data]

        data['_resource'] = resource_name
        return Model(**data)

    def _serialize(self, data):
        return encode_json(self.output_filter.filter(data))

    def _deserialize(self, data):
        return self.input_filter.filter(decode_json(data))

    def _handle_response(self, resource_name, data, status_code):
        data = self._deserialize(data)

        if status_code < 500:
            return self._modelize(resource_name, data)
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


class HttpNapClient(NapClient):

    def __init__(self, base_url, token=None):
        self.base_url = base_url
        self.timeout = 10
        self.token = token

    def _url_for(self, resource_name, path=''):
        url = self.base_url + self._endpoint_prefix(resource_name) + '/' + str(path)

        return url

    def call(self, resource_name, path='', method='GET', data=None):
        url = self._url_for(resource_name, path)

        method = getattr(requests, method.lower())
        if data:
            response = method(url, data=self._serialize(data), headers=self._headers(), timeout=self.timeout)
        else:
            response = method(url, headers=self._headers(), timeout=self.timeout)

        return self._handle_response(resource_name, response.content, response.status_code)
