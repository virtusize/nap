# -*- coding: utf-8 -*-

import copy
import urllib
import requests
from inflection import dasherize, underscore, pluralize
from flask_nap.view_filters import UnderscoreFilter, CamelizeFilter
from nap.model import Model
from nap.util import encode_json, decode_json


class Response(object):
    def __init__(self, resource, raw_data, status):
        self.status = status
        self.resource = resource
        self.raw_data = raw_data
        self.data = self._modelize() if raw_data else []

    @property
    def successful(self):
        return self.status in range(200,300)

    @property
    def first(self):
        if not self.successful or \
           isinstance(self.data, list) and len(self) == 0:
            return None

        if isinstance(self.data, list):
            return self[0]
        else:
            return self.data

    @property
    def error(self):
        if self.successful:
            return None

        return self.data

    def _modelize(self):
        if isinstance(self.raw_data, list):
            dct = copy.deepcopy(self.raw_data)
            for item in dct:
                item['_resource'] = self.resource

            return [Model(**item) for item in dct]

        dct = copy.deepcopy(self.raw_data)
        dct['_resource'] = self.resource
        return Model(**dct)

    def __str__(self):
        return str(self.__getstate__())

    def __repr__(self):
        return self.__class__.__name__ + '(**' + str(self) + ')'

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False

        return self.__getstate__() == other.__getstate__()

    def __ne__(self, other):
        return not self.__eq__(other)

    def __getstate__(self):
        d = self.__dict__.copy()
        for k in d.keys():
            if k.startswith('_'):
                del d[k]
        return d

    def __len__(self):
        if not self.successful:
            return 0
        
        if isinstance(self.data, list):
            return len(self.data)
        
        return 1

    def __getitem__(self, key):
        if not self.successful:
            return None 
        
        if isinstance(self.data, list):
            return self.data[key]
            
        return self.data


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


    def _serialize(self, data):
        return encode_json(self.output_filter.filter(data))

    def _deserialize(self, data):
        return self.input_filter.filter(decode_json(data))

    def _handle_response(self, resource_name, data, status_code):
        data = self._deserialize(data)

        if status_code < 500:
            return Response(resource_name, data, status_code)
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
