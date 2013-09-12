# -*- coding: utf-8 -*-

from functools import wraps

from nap.exceptions import ModelNotFoundException, UnsupportedMethodException, UnauthorizedException


class BaseController(object):

    def index(self, context=None):
        raise UnsupportedMethodException(model_name=self.model_name)

    def read(self, id, context=None):
        raise UnsupportedMethodException(model_name=self.model_name)

    def create(self, attributes, context=None):
        raise UnsupportedMethodException(model_name=self.model_name)

    def update(self, id, attributes, context=None):
        raise UnsupportedMethodException(model_name=self.model_name)

    def delete(self, id, context=None):
        raise UnsupportedMethodException(model_name=self.model_name)

    def query(self, query, context=None):
        raise UnsupportedMethodException(model_name=self.model_name)

    @property
    def model_name(self):
        return self.model.__name__ if hasattr(self, 'model') and self.model.__name__ else self.__class__.__name__


def fetch_instance(f):
    @wraps(f)
    def wrapper(controller, id, context=None):
        if not context:
            context = {}

        context['subject'] = controller._fetch_instance(id)

        return f(controller, id, context=context)

    return wrapper


def fetch_collection(f):
    @wraps(f)
    def wrapper(controller, context=None):
        if not context:
            context = {}

        context['subject'] = controller._fetch_collection()

        return f(controller, context=context)

    return wrapper


def authorize(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if len(args) == 1:
            controller, = args
        elif len(args) == 2:
            controller, id = args

        if 'context' in kwargs and\
           'identity' in kwargs['context'] and\
           'subject' in kwargs['context'] and\
           controller.guard:
            if controller.guard.cannot(kwargs['context']['identity'], f.__name__, kwargs['context']['subject']):
                raise UnauthorizedException(controller.model_name)

        return f(*args, **kwargs)

    return wrapper


class ModelController(BaseController):

    @fetch_collection
    @authorize
    def index(self, context=None):
        return context['subject']

    @fetch_instance
    @authorize
    def read(self, id, context=None):
        if context['subject']:
            return context['subject']
        else:
            raise ModelNotFoundException(model_id=id, model_name=self.model_name)

    def _fetch_instance(self, id):
        return self.model_storage._get(id)

    def _fetch_collection(self):
        return self.model_storage._all()
