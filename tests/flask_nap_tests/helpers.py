# -*- coding: utf-8 -*-

from fixtures import app
from nap.util import encode_json, decode_json

test_client = app.test_client()


def request_context():
    return RequestContext()


class RequestContext(object):
    """
    Creates a request stack so that url_for and requests can be made.
    """

    def __enter__(self):
        self._ctx = app.test_request_context()
        self._ctx.push()

    def __exit__(self, type, value, traceback):
        if hasattr(self, '_ctx'):
            self._ctx.pop()


def _augment_response_class(response_class):

    class JsonResponseMixin(object):
        """
        Mixin with testing helper methods
        """
        @property
        def json(self):
            return decode_json(self.data)

    class TestResponse(response_class, JsonResponseMixin):
        pass

    return TestResponse

app.response_class = _augment_response_class(app.response_class)


def with_json_data(dct):
    return dict(data=encode_json(dct), content_type='application/json')
