# -*- coding: utf-8 -*-

from flask.json import JSONDecoder
from api_fixtures import app

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
            return JSONDecoder().decode(self.data)

    class TestResponse(response_class, JsonResponseMixin):
        pass

    return TestResponse

app.response_class = _augment_response_class(app.response_class)
