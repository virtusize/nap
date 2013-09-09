# -*- coding: utf-8 -*-

from nap.exceptions import ModelNotFoundException, UnsupportedMethodException


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


class ModelController(BaseController):

    def index(self, context=None):
        return self.model_storage._all()

    def read(self, id, context=None):
        model = self.model_storage._get(id)
        if model:
            return model
        else:
            raise ModelNotFoundException(model_id=id, model_name=self.model_name)

