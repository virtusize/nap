# -*- coding: utf-8 -*-

from core.model.serialization import dict_or_state
from core.validation import ValidationMetaClass, ValidationMixin


class Model(ValidationMixin):

    __metaclass__ = ValidationMetaClass

    def __init__(self, *args, **kwargs):
        self.__dict__.update(kwargs)

    def to_dict(self, strategy=dict_or_state):
        return strategy(self)


class Storage:

    @classmethod
    def _all(cls):
        return [v for k, v in cls.__dict__.items() if not k.startswith('_')]

    @classmethod
    def _get(cls, id):
        return cls._get_by('id', id)

    @classmethod
    def _get_by(cls, key, value):
        for model in cls.__dict__.values():
            if hasattr(model, key) and getattr(model, key) == value:
                return model
        return None
