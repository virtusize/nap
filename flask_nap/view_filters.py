#!/usr/bin/python
# -*- coding: utf-8 -*-
from inflection import camelize, underscore


class Filter(object):

    def __init__(self):
        pass

    def filter(self, dct, ctx):
        raise NotImplementedError


class KeyFilter(Filter):

    def __init__(self, key_filter):
        self.key_filter = key_filter

    def filter(self, dct, ctx=None):
        if isinstance(dct, list):
            res = []
            for item in dct:
                res.append({self.key_filter(k): v for (k, v) in item.items()})

            return res

        return {self.key_filter(k): v for (k, v) in dct.items()}


class CamelizeFilter(KeyFilter):

    def __init__(self, uppercase_first_letter=False):
        super(CamelizeFilter, self).__init__(lambda k: camelize(k, uppercase_first_letter))


class UnderscoreFilter(KeyFilter):

    def __init__(self):
        super(UnderscoreFilter, self).__init__(lambda k: underscore(k))


class ExcludeFilter(Filter):

    def __init__(self, exclude):
        self.exclude = exclude

    def filter(self, dct, ctx=None):
        return {k: v for (k, v) in dct.items() if not k in self.exclude}


class ExcludeActionFilter(ExcludeFilter):

    def __init__(self, exclude, action, guard):
        self.exclude = exclude
        self.action = action
        self.guard = guard

    def filter(self, dct, ctx):
        if self.guard.cannot(ctx.identity, self.action, ctx.subject):
            return super(ExcludeActionFilter, self).filter(dct, ctx)

        return dct
