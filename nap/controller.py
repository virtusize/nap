# -*- coding: utf-8 -*-

from nap.exceptions import ModelNotFoundException, UnsupportedMethodException, UnauthorizedException


class BaseController(object):

    def index(self, ctx=None):
        raise UnsupportedMethodException(model_name=self.model_name)

    def read(self, id, ctx=None):
        raise UnsupportedMethodException(model_name=self.model_name)

    def create(self, attributes, ctx=None):
        raise UnsupportedMethodException(model_name=self.model_name)

    def update(self, id, attributes, ctx=None):
        raise UnsupportedMethodException(model_name=self.model_name)

    def delete(self, id, ctx=None):
        raise UnsupportedMethodException(model_name=self.model_name)

    def query(self, query, ctx=None):
        raise UnsupportedMethodException(model_name=self.model_name)

    @property
    def model_name(self):
        return self.model.__name__ if hasattr(self, 'model') and self.model.__name__ else self.__class__.__name__

    def authorize(self, ctx, action, model_or_list):
        if not hasattr(self, 'guard'):
            return model_or_list

        elif not ctx or 'identity' not in ctx:
            raise UnauthorizedException(self.model_name)

        if self.guard.cannot(ctx.identity, action, model_or_list):
            raise UnauthorizedException(self.model_name)

        return model_or_list


class ModelController(BaseController):

    def index(self, ctx=None):
        return self.authorize(ctx, 'read', self.fetch_all())

    def read(self, id, ctx=None):
        return self.authorize(ctx, 'read', self.fetch_model(id))

    def fetch_model(self, id):
        model = self.model_storage._get(id)

        if not model:
            raise ModelNotFoundException(model_id=id, model_name=self.model_name)

        return model

    def fetch_all(self):
        return self.model_storage._all()
