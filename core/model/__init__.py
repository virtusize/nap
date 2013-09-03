# -*- coding: utf-8 -*-

from inflection import underscore, pluralize
from core.model.serialization import dict_or_state
from core.validation import ValidationMetaClass, ValidationMixin


class Model(object):

    @classmethod
    def api_name(cls):
        """
        Convert CamelCase class name to underscores_between_words (plural) table name.
        """
        return underscore(pluralize(cls.__name__))

    def to_dict(self, strategy=dict_or_state):
        return strategy(self)


class SimpleModel(Model, ValidationMixin):

    __metaclass__ = ValidationMetaClass

    def __init__(self, *args, **kwargs):
        self.__dict__.update(kwargs)


class SimpleModelStore():

    def __init__(self, model_cls):
        self._model_cls = model_cls
        self.clear()

    def add(self, model):
        self._check_model(model)

        self._store[model.id] = model

    def add_all(self, models):
        for model in models:
            self.add(model)

    def get_all(self):
        return self._store.values()

    def get(self, id):
        return self._store[id]

    def get_by(self, key, value):
        for model in self._store.values():
            dct = model.to_dict()
            if key in dct and dct[key] == value:
                return model
        return None

    def delete(self, id):
        if id in self._store:
            del(self._store[id])

    def clear(self):
        self._store = {}

    def count(self):
        return len(self._store)

    def empty(self):
        return self.count() == 0

    def next_id(self):
        return 1 if self.empty() else max(self._store.keys())+1

    def _check_model(self, model):
        if not isinstance(model, SimpleModel):
            raise TypeError('Model must be of type SimpleModel')

        if not isinstance(model, self._model_cls):
            raise TypeError('Model must be of type %s' % self._model_cls.__name__)

        if hasattr(model, 'id'):
            if model.id in self._store:
                raise UserWarning('A model with id %s already exists in this store' % model.id)
        else:
            model.id = self.next_id()
