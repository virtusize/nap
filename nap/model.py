# -*- coding: utf-8 -*-
from nap.validation import ValidationMetaClass, ValidationMixin


class BaseModel(ValidationMixin):
    pass


class Model(BaseModel):

    __metaclass__ = ValidationMetaClass

    def __init__(self, *args, **kwargs):
        self.__dict__.update(kwargs)


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

    @classmethod
    def _pluck(cls, key='id'):
        return [getattr(item, key, None) for item in cls._all()]


class BaseSerializer(object):

    def serialize(self, subject):
        raise NotImplementedError


class ModelSerializer(BaseSerializer):

    def serialize(self, subject):
        return subject.__dict__
