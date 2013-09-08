#!/usr/bin/python
# -*- coding: utf-8 -*-
from inflection import camelize


class Filter(object):

    def __init__(self):
        pass

    def filter(self, dct):
        raise NotImplementedError


class KeyFilter(Filter):

    def __init__(self, key_filter):
        self.key_filter = key_filter

    def filter(self, dct):
        return {self.key_filter(k): v for (k, v) in dct.items()}


class CamelizeFilter(KeyFilter):

    def __init__(self, uppercase_first_letter=False):
        super(CamelizeFilter, self).__init__(lambda k: camelize(k, uppercase_first_letter))


class ExcludeFilter(Filter):

    def __init__(self, exclude=[]):
        self.exclude = exclude

    def filter(self, dct):
        return {k: v for (k, v) in dct.items() if not k in self.exclude}
