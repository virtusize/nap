#!/usr/bin/python
# -*- coding: utf-8 -*-

from nap.util import Declarative
from tests.helpers import compare


def test_with_meta():
    #Classic way to define metaclasses
    class MetaTest(type):
        def __new__(mcs, class_name, bases, attr):
            attr['foo'] = 'bar'
            return type.__new__(mcs, class_name, bases, attr)

    class A(object):
        __metaclass__ = MetaTest

    compare(A.foo, 'bar')
    compare(A().foo, 'bar')

    #Shorter way, using util.Declarative
    class B(Declarative):
        def __classinit__(cls, attr):
            setattr(cls, 'foo', 'bar')
            pass

    compare(B.foo, 'bar')
    compare(B().foo, 'bar')
