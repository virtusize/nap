#!/usr/bin/python
# -*- coding: utf-8 -*-

import re

from sqlalchemy.ext.declarative import declarative_base, declared_attr


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


class DbModel(Model):
    """
    Base class for DB Models
    """
    @declared_attr
    def __tablename__(cls):
        """
        Convert CamelCase class name to underscores_between_words (plural) table name.
        """
        name = cls.__name__
        return (
            name[0].lower() +
            re.sub(r'([A-Z])', lambda m: "_" + m.group(0).lower(), name[1:]) + 's'
        )

DbModel = declarative_base(cls=DbModel)
