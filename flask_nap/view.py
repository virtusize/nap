# -*- coding: utf-8 -*-
import inspect
from collections import Iterable
from functools import wraps
from itertools import imap
from flask import g
from inflection import dasherize, underscore, pluralize
from nap.model import BaseModel
from nap.util import ensure_instance

DEFAULT_METHODS_MAPPING = dict(
    get=['GET'],
    put=['PUT'],
    post=['POST'],
    patch=['PATCH'],
    delete=['DELETE'],
    index=['GET'],
    query=['GET']
)


def route(rule, **options):

    def decorator(f):
        options['rule'] = rule
        setattr(f, '_route_options', options)
        return f

    return decorator


class InvalidRuleError(RuntimeError):
    pass


class BaseView(object):
    #endpoint_prefix

    def _register_on(self, api):

        for func_name, func in inspect.getmembers(self, predicate=inspect.ismethod):
            if not hasattr(func, '_route_options'):
                continue

            #Make a copy of the options
            options = dict(getattr(func, '_route_options'))

            if not 'endpoint' in options:
                options['endpoint'] = self.endpoint_prefix + '_' + func_name

            if not 'methods' in options:
                options['methods'] = DEFAULT_METHODS_MAPPING.get(func_name, ['GET'])

            rule = options.pop('rule', False)
            if not rule:
                raise InvalidRuleError('%s is missing a rule' % func_name)
            rule = rule.format(**self.__dict__)
            print rule + ' -> ' + str(options)
            options['view_func'] = self.make_view(api, func)

            api.add_url_rule(rule, **options)

    def make_view(self, api, func):

        @wraps(func)
        def wrapper(*args, **kwargs):
            return api.make_response(func(*args, **kwargs))

        return wrapper


class ModelView(BaseView):

    def __init__(self):
        cls = self.__class__
        self.controller = ensure_instance(cls.controller)
        self.serializer = ensure_instance(cls.serializer)
        self.filter_chain = [ensure_instance(f) for f in cls.filter_chain]
        self.endpoint_prefix = cls.endpoint_prefix if hasattr(cls, 'endpoint_prefix') else underscore(pluralize(self.controller.model.__name__))
        self.dashed_endpoint = dasherize(self.endpoint_prefix)

    def filter(self, subject):

        def apply_filter_chain(m):
            dct = self.serializer.serialize(m)

            for filter in self.filter_chain:
                dct = filter.filter(dct, g.ctx)

            return dct

        if isinstance(subject, BaseModel):
            return apply_filter_chain(subject)
        elif isinstance(subject, Iterable):
            return list(imap(apply_filter_chain, subject))
        else:
            raise TypeError('Filters expect the objects to be of type BaseModel')

    def make_view(self, api, func):

        @wraps(func)
        def wrapper(*args, **kwargs):
            data, code = func(*args, **kwargs)
            data = self.filter(data)
            return api.make_response(data, code)

        return wrapper

    @route('/{dashed_endpoint}/')
    def index(self):
        return self.controller.index(g.ctx), 200

    @route('/{dashed_endpoint}/<int:id>')
    def get(self, id):
        return self.controller.read(id, g.ctx), 200

    @route('/{dashed_endpoint}/')
    def post(self):
        return self.controller.create(g.ctx.input, g.ctx), 201

    @route('/{dashed_endpoint}/<int:id>')
    def put(self, id):
        return self.controller.update(id, g.ctx.input, g.ctx), 200

    @route('/{dashed_endpoint}/<int:id>')
    def patch(self, id):
        return self.controller.update(id, g.ctx.input, g.ctx), 200

    @route('/{dashed_endpoint}/<int:id>')
    def delete(self, id):
        return self.controller.delete(id, g.ctx), 200
