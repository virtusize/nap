# -*- coding: utf-8 -*-

import re

from core.model.serialization import dict_or_state
from core.validation import ValidationMetaClass, ValidationMixin


class Model(object):

    @classmethod
    def api_name(cls):
        """
        Convert CamelCase class name to underscores_between_words (plural) table name.
        """
        name = cls.__name__
        return (
            name[0].lower() +
            re.sub(r'([A-Z])', lambda m: "_" + m.group(0).lower(), name[1:]) + 's'
        )

    def to_dict(self, strategy=dict_or_state):
        return strategy(self)


class SimpleModel(Model, ValidationMixin):

    __metaclass__ = ValidationMetaClass

    def __init__(self, *args, **kwargs):
        self.__dict__.update(kwargs)
