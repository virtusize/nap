#!/usr/bin/python
# -*- coding: utf-8 -*-
import datetime
import uuid

from nap.util import ensure_instance, Context, encode_json, decode_json
from tests.helpers import *


def test_ensure_instance():
    class A(object):
        pass

    class B:
        pass

    a = A()
    b = B()

    assert_true(isinstance(ensure_instance(a), A))
    assert_true(isinstance(ensure_instance(A), A))
    assert_true(isinstance(ensure_instance(b), B))
    assert_true(isinstance(ensure_instance(B), B))


def test_ctx():
    ctx = Context()
    assert_is_none(ctx.not_existing)
    assert_is_none(ctx['not_existing'])
    assert_false('not_existing' in ctx)

    ctx.something = 'foo'

    assert_equal(ctx.something, 'foo')
    assert_equal(ctx.something, ctx['something'])
    assert_true('something' in ctx)

    ctx['something'] = 'bar'

    assert_equal(ctx.something, 'bar')
    assert_equal(ctx.something, ctx['something'])
    assert_true('something' in ctx)

    compare(list(ctx), ctx.__dict__.keys())


def test_json():
    s = '[0, true, "False"]'
    compare(s, encode_json([0, True, 'False']))
    compare(s, encode_json(decode_json(s)))

    d = {'one': 0, 'two': True, 'three': 'False'}
    s = '{"three": "False", "two": true, "one": 0}'
    compare(s, encode_json(d))
    compare(d, decode_json(encode_json(d)))


def test_json_encoder():
    now = datetime.datetime.utcnow()
    date = now.date()
    time = now.time()
    uid = uuid.uuid4()

    obj = {
        'datetime': now,
        'date': date,
        'time': time,
        'uuid': uid
    }

    expected = {
        'datetime': now.isoformat(),
        'date': date.isoformat(),
        'time': time.isoformat(),
        'uuid': str(uid)
    }

    compare(expected, decode_json(encode_json(obj)))