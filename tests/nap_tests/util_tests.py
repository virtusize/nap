#!/usr/bin/python
# -*- coding: utf-8 -*-

from nap.util import ensure_instance, Context
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
