# -*- coding: utf-8 -*-
from nap.model import Model, Storage
from nap.util import Declarative


class BaseController(Declarative):

    def index(self, context=None):
        raise NotImplementedError

    def read(self, id, context=None):
        raise NotImplementedError

    def create(self, attributes, context=None):
        raise NotImplementedError

    def update(self, id, attributes, context=None):
        raise NotImplementedError

    def delete(self, id, context=None):
        raise NotImplementedError

    def query(self, query, context=None):
        raise NotImplementedError


class ModelController(BaseController):

    def index(self, context=None):
        return self.model_storage._all()

    def read(self, id, context=None):
        return self.model_storage._get(id)

