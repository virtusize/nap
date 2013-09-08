#!/usr/bin/python
# -*- coding: utf-8 -*-


class DeclarativeMeta(type):
    def __new__(mcs, class_name, bases, new_attrs):
        cls = type.__new__(mcs, class_name, bases, new_attrs)
        cls.__classinit__.im_func(cls, new_attrs)
        return cls


class Declarative(object):
    """
    Subclass this class if you need custom stuff done each time
    your class is subclassed.

    Usage:
    class A(Declarative):
        def __classinit__(cls, attr):
            #cls is the new class,
            #attr are the attributes of the new class.
    """
    __metaclass__ = DeclarativeMeta

    def __classinit__(cls, attr):
        pass
