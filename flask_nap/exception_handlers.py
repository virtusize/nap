# -*- coding: utf-8 -*-
from flask import g
from flask.ext.nap.api import InvalidJSONException

from flask_nap.view_filters import CamelizeFilter
from nap.exceptions import UnsupportedMethodException, ModelNotFoundException, ModelInvalidException, UnauthenticatedException, UnauthorizedException, InvalidMimetypeException


class NapExceptionHandler(object):

    def _register_on(self, api):
        self.api = api
        api.errorhandler(self.exception)(self.handle_exception)

    def handle_exception(self, error):
        dct = error.to_dict()
        dct['status_code'] = self.status_code
        dct = CamelizeFilter().filter(dct)

        return self.api.make_response(dct, self.status_code)


class UnauthenticatedExceptionHandler(NapExceptionHandler):
    exception = UnauthenticatedException
    status_code = 401


class UnauthorizedExceptionHandler(NapExceptionHandler):
    exception = UnauthorizedException
    status_code = 403


class UnsupportedMethodExceptionHandler(NapExceptionHandler):
    exception = UnsupportedMethodException
    status_code = 405


class ModelNotFoundExceptionHandler(NapExceptionHandler):
    exception = ModelNotFoundException
    status_code = 404


class ModelInvalidExceptionHandler(NapExceptionHandler):
    exception = ModelInvalidException
    status_code = 422


class InvalidJSONExceptionHandler(NapExceptionHandler):
    exception = InvalidJSONException
    status_code = 400


class InvalidMimetypeExceptionHandler(NapExceptionHandler):
    exception = InvalidMimetypeException
    status_code = 415


class HTTPExceptionHandler(NapExceptionHandler):
    def __init__(self, app, api, code):
        self.app = app
        self.api = api
        self.code = code
        app.errorhandler(self.code)(self.handle_exception)

    def handle_exception(self, error):
        message = error.name if hasattr(error, 'name') else str(error)
        dct = {'message': message, 'status_code': self.code}
        dct = CamelizeFilter().filter(dct)

        return self.api.make_response(dct, self.code)

    @classmethod
    def register_on(cls, app, api):
        for code in range(400, 503):
            HTTPExceptionHandler(app, api, code)
