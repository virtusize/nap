#!/usr/bin/python
# -*- coding: utf-8 -*-

import types
import json
import datetime
import uuid


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


class JSONEncoder(json.JSONEncoder):

    def default(self, o):
        """
        Allows serialization of datetime objects and uuid
        """
        if isinstance(o, (datetime.datetime, datetime.date, datetime.time)):
            return o.isoformat()
        if isinstance(o, uuid.UUID):
            return str(o)
        return json.JSONEncoder.default(self, o)


json_encoder = JSONEncoder()
json_decoder = json.JSONDecoder()


def encode_json(data):
    return json_encoder.encode(data)


def decode_json(data):
    return json_decoder.decode(data)
