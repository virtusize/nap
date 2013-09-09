# -*- coding: utf-8 -*-
from flask import current_app, g

from nap.exceptions import UnsupportedMethodException, ModelNotFoundException, ModelInvalidException
from nap.util import ensure_instance


class NapExceptionHandler(object):

    @classmethod
    def _register_on(cls, api):
        handler = ensure_instance(cls)
        api.errorhandler(cls.exception)(handler.handle_exception)

    def handle_exception(self, error):
        dct = error.to_dict()
        dct['status_code'] = self.status_code
        data = g.get('data_encoder').encode(dct)
        response = current_app.make_response(data)
        response.status_code = self.status_code
        return response


class UnsupportedMethodExceptionHandler(NapExceptionHandler):
    exception = UnsupportedMethodException
    status_code = 405


class ModelNotFoundExceptionHandler(NapExceptionHandler):
    exception = ModelNotFoundException
    status_code = 404


class ModelInvalidExceptionHandler(NapExceptionHandler):
    exception = ModelInvalidException
    status_code = 422

