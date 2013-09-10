# -*- coding: utf-8 -*-
from flask import current_app, g

from nap.exceptions import UnsupportedMethodException, ModelNotFoundException, ModelInvalidException
from nap.util import ensure_instance


class NapExceptionHandler(object):

    def _register_on(self, api):
        self.api = api
        api.errorhandler(self.exception)(self.handle_exception)

    def handle_exception(self, error):
        dct = error.to_dict()
        dct['status_code'] = self.status_code

        return self.api.make_response(dct, self.status_code)


class UnsupportedMethodExceptionHandler(NapExceptionHandler):
    exception = UnsupportedMethodException
    status_code = 405


class ModelNotFoundExceptionHandler(NapExceptionHandler):
    exception = ModelNotFoundException
    status_code = 404


class ModelInvalidExceptionHandler(NapExceptionHandler):
    exception = ModelInvalidException
    status_code = 422

