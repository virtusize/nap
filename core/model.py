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



