#!/usr/bin/python
# -*- coding: utf-8 -*-

import types
from flask.json import JSONEncoder, JSONDecoder


def ensure_instance(cls_or_instance):
    """
    Makes sure that we always have an instance,
    if passed a class, assume it has a default constructor
    and instantiate it.
    """
    if isinstance(cls_or_instance, (type, types.ClassType)):
        return cls_or_instance()
    else:
        return cls_or_instance


class Context(object):
    """A plain object."""

    def get(self, name, default=None):
        return self.__dict__.get(name, default)

    def __contains__(self, item):
        return item in self.__dict__

    def __iter__(self):
        return iter(self.__dict__)

    def __getattr__(self, attr):
        return self.get(attr)

    def __getitem__(self, key):
        return self.get(key)

    def __setitem__(self, key, value):
        self.__dict__[key] = value


json_encoder = JSONEncoder()
json_decoder = JSONDecoder()


def encode_json(data):
    return json_encoder.encode(data)


def decode_json(data):
    return json_decoder.decode(data)
