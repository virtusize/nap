# -*- coding: utf-8 -*-

import pprint
from itertools import imap
from functools import wraps
from collections import Iterable

from inflection import underscore, dasherize, pluralize
from flask import Blueprint, request, g
from flask.json import JSONEncoder
from flask.views import MethodView

from nap.model import BaseModel


class Api(Blueprint):

    def __init__(self, name, prefix, version):
        super(Api, self).__init__(name, name,
                                  url_prefix=prefix + '/v' + str(version))


class ApiMixin(object):

    def __init__(self, api):
        api.before_request(self.before)
        api.after_request(self.after)

    def before(self):
        pass

    def after(self, response):
        return response


class Debug(ApiMixin):

    def __init__(self, api, print_request=True, print_response=True):
        super(Debug, self).__init__(api)
        self.print_request = print_request
        self.print_response = print_response

    def before(self):
        request_info = {}

        request_fields = ['method','content_type', 'data', 'values', 'cookies', 'headers', 'path', 'full_path',
                          'script_root', 'url', 'base_url', 'url_root', 'host_url', 'host',  'remote_addr']

        for field in request_fields:
            request_info[field] = unicode(getattr(request, field, None))
        
        g.debug = True
        if self.print_request:
            pprint.pprint(request_info)
            
    def after(self, response):
        if self.print_response:
            print str(dir(response))
        return response


class JsonEncoder(ApiMixin):
    def __init__(self, api):
        super(JsonEncoder, self).__init__(api)
        self.encoder = JSONEncoder()

    def before(self):
        g.data_encoder = self.encoder


class JsonDecoder(ApiMixin):
    def before(self):
        g.incoming_data = request.get_json()


class MethodOverride(ApiMixin):
    pass


class Authentication(ApiMixin):
    pass


class BaseApiView(object):

    def __init__(self, endpoint, id_type='int'):
        self.endpoint = endpoint
        self.route_prefix = '/' + dasherize(self.endpoint) + '/'
        self.id_type = id_type

    def index(self):
        raise NotImplementedError

    def get(self, id):
        raise NotImplementedError

    def post(self):
        raise NotImplementedError

    def put(self, id):
        raise NotImplementedError

    def patch(self, id):
        raise NotImplementedError

    def delete(self, id):
        raise NotImplementedError

    def register_on(self, api):

        api.add_url_rule(self.route_prefix, endpoint=self.endpoint + '_index',
                         view_func=self._wrap(self.index), methods=['GET'])

        api.add_url_rule(self.route_prefix + '<%s:id>' % self.id_type, endpoint=self.endpoint + '_get',
                         view_func=self._wrap(self.get), methods=['GET'])

        api.add_url_rule(self.route_prefix, endpoint=self.endpoint + '_post',
                         view_func=self._wrap(self.post), methods=['POST'])

        api.add_url_rule(self.route_prefix + '<%s:id>' % self.id_type, endpoint=self.endpoint + '_put',
                         view_func=self._wrap(self.put), methods=['PUT'])

        api.add_url_rule(self.route_prefix + '<%s:id>' % self.id_type, endpoint=self.endpoint + '_patch',
                         view_func=self._wrap(self.patch), methods=['PATCH'])

        api.add_url_rule(self.route_prefix + '<%s:id>' % self.id_type, endpoint=self.endpoint + '_delete',
                         view_func=self._wrap(self.delete), methods=['DELETE'])

    def _wrap(self, f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            # Do before request
            response = f(*args, **kwargs)
            # Do after request
            if g.get('data_encoder', None):
                response = g.get('data_encoder').encode(response)

            return response

        return wrapper


class Filter(object):

    def fiter(self, dct):
        raise NotImplementedError


class ModelView(BaseApiView):

    def __init__(self, controller, serializer, filter_chain=[], id_type='int'):
        endpoint = underscore(pluralize(controller.model.__name__))
        super(ModelView, self).__init__(endpoint, id_type)
        self.controller = controller
        self.serializer = serializer
        self.filter_chain = filter_chain

    def _apply_filters(self, subject):

        def apply_filter_chain(m):
            dct = self.serializer.serialize(m)

            for filter in self.filter_chain:
                dct = filter.filter(dct)

            return dct

        if isinstance(subject, BaseModel):
            return apply_filter_chain(subject)
        elif isinstance(subject, Iterable):
            return list(imap(apply_filter_chain, subject))
        else:
            raise TypeError('Filters expect the objects to be of type BaseModel')

    def index(self):
        return self._apply_filters(self.controller.index())

    def get(self, id):
        return self._apply_filters(self.controller.read(id))

    def post(self):
        return self._apply_filters(self.controller.create(g.incoming_data))

    def put(self, id):
        s = self.controller.update(id, g.incoming_data)
        d = self._apply_filters(s)

        return d

    def patch(self, id):
        return self._apply_filters(self.controller.update(id, g.incoming_data))

    def delete(self, id):
        return self._apply_filters(self.controller.delete(id))
