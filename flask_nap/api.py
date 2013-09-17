# -*- coding: utf-8 -*-
import pprint
from flask import Blueprint, request, g, make_response
from flask.json import JSONEncoder, JSONDecoder
from nap.exceptions import NapException
from nap.util import ensure_instance, Context


class Api(Blueprint):

    def __init__(self):
        super(Api, self).__init__(self.name, self.name, url_prefix=self.prefix + '/v' + str(self.version))
        self.before_request(self.setup_ctx)

        self.mixins = [ensure_instance(m) for m in self.mixins]
        for m in self.mixins:
            m._register_on(self)

        self.views = [ensure_instance(v) for v in self.views]
        for v in self.views:
            v._register_on(self)

        self.exception_handlers = [ensure_instance(v) for v in self.exception_handlers]
        for v in self.exception_handlers:
            v._register_on(self)

    def make_response(self, data, status_code):
        json_data = JSONEncoder().encode(data)
        response = make_response(json_data)
        response.status_code = status_code
        response.mimetype = 'application/json'
        return response

    def setup_ctx(self):
        g.ctx = Context()


class ApiMixin(object):

    def _register_on(self, api):
        api.before_request(self.before)
        api.after_request(self.after)

    def before(self):
        pass

    def after(self, response):
        return response


class Debug(ApiMixin):

    def __init__(self, print_request=True, print_response=True):
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


class InvalidJSONException(NapException):

    def __init__(self, data):
        super(InvalidJSONException, self).__init__(message='Mime-type is JSON, but no JSON object could be decoded.', data=data)


class JsonRequestParser(ApiMixin):

    decoder = JSONDecoder()

    def before(self):
        input = None

        if request.mimetype == 'application/json' and request.content_length:
            try:
                input = self.decoder.decode(request.data)
            except:
                raise InvalidJSONException(request.data)

        g.ctx.input = input
