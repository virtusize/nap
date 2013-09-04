# -*- coding: utf-8 -*-


class BaseController(object):

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

    def __init__(self, model, model_storage):
        self.model = model
        self.model_storage = model_storage

    def index(self, context=None):
        return self.model_storage._all()

    def read(self, id, context=None):
        return self.model_storage._get(id)

