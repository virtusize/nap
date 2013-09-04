# -*- coding: utf-8 -*-

import pprint

from inflection import underscore, dasherize, pluralize
from flask import Blueprint, request, g
from flask.json import JSONEncoder
from flask.views import MethodView


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

        request_fields = ['values', 'cookies', 'headers', 'path', 'full_path',
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
    pass


class MethodOverride(ApiMixin):
    pass


class Authentication(ApiMixin):
    pass


class ModelView(MethodView):
    id_type = 'int'

    @classmethod
    def endpoint(cls):
        return '/' + dasherize(cls.model_name()) + '/'

    @classmethod
    def model_name(cls):
        return underscore(pluralize(cls.model.__name__))

    @classmethod
    def register_on(cls, api):
        view = cls.as_view(cls.model_name())
        endpoint_prefix = cls.endpoint()

        api.add_url_rule(endpoint_prefix, defaults={'id': None},
                          view_func=view, methods=['GET'])

        api.add_url_rule(endpoint_prefix,
                          view_func=view, methods=['POST'])

        api.add_url_rule(endpoint_prefix + '<%s:id>' % cls.id_type,
                          view_func=view, methods=['GET', 'PUT', 'DELETE'])

        api.add_url_rule(endpoint_prefix, view_func=view)

    
    def dispatch_request(self, *args, **kwargs):
        meth = getattr(self, request.method.lower(), None)
        # if the request method is HEAD and we don't have a handler for it
        # retry with GET
        if meth is None and request.method == 'HEAD':
            meth = getattr(self, 'get', None)
        assert meth is not None, 'Unimplemented method %r' % request.method
        data = meth(*args, **kwargs)
        return g.data_encoder.encode(data)


class ImplicitModelView(ModelView):

    def get(self, id=None):
        if id is None:
            return [m.to_dict() for m in self.store._all()]
        else:
            return self.store._get(id).to_dict()
