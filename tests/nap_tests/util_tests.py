#!/usr/bin/python
# -*- coding: utf-8 -*-

from nap.util import ensure_instance
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