# -*- coding: utf-8 -*-
from core.authorization import Guard
from core.model.serialization import dict_or_state
from core.validation import ValidationMetaClass, ValidationMixin


class Model(object):

    def to_dict(self, strategy=dict_or_state):
        return strategy(self)


class SimpleModel(Model, ValidationMixin):

    __metaclass__ = ValidationMetaClass

    def __init__(self, *args, **kwargs):
        self.__dict__.update(kwargs)


class ModelGuard(Guard):

    def can(self, identity, action, model_instance, **kwargs):
        return False


class Actions:
    create = 'create'
    read = 'read'
    update = 'update'
    delete = 'delete'