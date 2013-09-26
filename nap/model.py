# -*- coding: utf-8 -*-
from nap.validation import ValidationMetaClass, ValidationMixin


class BaseModel(ValidationMixin):
    pass


class Model(BaseModel):

    __metaclass__ = ValidationMetaClass

    def __init__(self, *args, **kwargs):
        self.__dict__.update(kwargs)

    def __str__(self):
        return str(self.__getstate__())

    def __repr__(self):
        return self.__class__.__name__ + '(**' + str(self) + ')'

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False

        return self.__getstate__() == other.__getstate__()

    def __ne__(self, other):
        return not self.__eq__(other)

    def __getstate__(self):
        d = self.__dict__.copy()
        for k in d.keys():
            if k.startswith('_'):
                del d[k]
        return d


class Storage(object):

    @classmethod
    def _all(cls):
        items = [v for k, v in cls.__dict__.items() if not k.startswith('_')]

        if all([hasattr(e, 'id') for e in items]):
            items = sorted(items, key=lambda item: getattr(item, 'id'))

        return items

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
        return subject.__getstate__()
