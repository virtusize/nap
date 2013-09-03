# -*- coding: utf-8 -*-

import re

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
