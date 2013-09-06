# -*- coding: utf-8 -*-
import pprint
from flask import Blueprint, request, g
from flask.json import JSONEncoder


class Api(Blueprint):

    def __init__(self, name, prefix, version):
        super(Api, self).__init__(name, name, url_prefix=prefix + '/v' + str(version))


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
