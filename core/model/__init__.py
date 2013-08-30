# -*- coding: utf-8 -*-
from core.validation import ValidationMetaClass, ValidationMixin


class Model(object):

    @classmethod
    def _create(cls, data, context):
        raise NotImplementedError()

    @classmethod
    def _read(cls, id, context):
        raise NotImplementedError()

    @classmethod
    def _update(cls, id, data, context):
        raise NotImplementedError()

    @classmethod
    def _delete(cls, id, context):
        raise NotImplementedError()

    def to_dict(self):
        return self.__dict__


class SimpleModel(Model, ValidationMixin):

    __metaclass__ = ValidationMetaClass

    def __init__(self, *args, **kwargs):
        self.__dict__.update(kwargs)
