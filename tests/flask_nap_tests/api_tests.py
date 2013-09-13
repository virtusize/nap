# -*- coding: utf-8 -*-
from flask import g, request

from nap.util import Context
from flask_nap.api import ApiMixin, Debug, JsonDecoder
from tests.flask_nap_tests.fixtures import AnApi
from tests.flask_nap_tests.helpers import app
from tests.helpers import *


def test_api_init():
    an_api = AnApi()
    assert_equal(an_api.url_prefix, '/api/v1')
    assert_equal(an_api.name, 'api')
    assert_equal(an_api.import_name, 'api')


def test_api_mixin():
    mixin = ApiMixin()
    mixin.before()


def test_debug_mixin():
    with app.test_request_context('/'):
        assert_is_none(g.get('debug'))

        mixin = Debug()
        mixin.before()
        assert_true(g.get('debug'))

        mixin.after({})


def test_json_decoder_mixin():
    with app.test_request_context('/?one=1'):
        g.ctx = Context()

        def get_json():
            return {'one': 1, 'two': '2'}

        request.get_json = get_json

        mixin = JsonDecoder()
        mixin.before()

        compare(g.ctx.input, {'one': 1, 'two': '2'})
