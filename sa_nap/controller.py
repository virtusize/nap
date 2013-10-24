# -*- coding: utf-8 -*-
from nap.exceptions import ModelNotFoundException
from nap.controller import BaseController
from blinker import signal


class SAModelController(BaseController):

    def __init__(self):
        self.created = signal('resource-' + self.model._underscore_name() + '-created')
        self.updated = signal('resource-' + self.model._underscore_name() + '-updated')
        self.deleted = signal('resource-' + self.model._underscore_name() + '-deleted')

    def index(self, ctx=None):
        return self.authorize(ctx, 'index', self.fetch_all())

    def read(self, id, ctx=None):
        return self.authorize(ctx, 'read', self.fetch_model(id))

    def create(self, attributes, ctx=None):
        model = self.model(**attributes)
        self.authorize(ctx, 'create', model)
        self.db_session.add(model)
        self.db_session.commit()
        self.created.send(model)
        return model

    def update(self, id, attributes, ctx=None):
        model = self.authorize(ctx, 'update', self.fetch_model(id))
        model.update_attributes(attributes)
        self.db_session.commit()
        self.updated.send(model)
        return model

    def delete(self, id, ctx=None):
        model = self.authorize(ctx, 'delete', self.fetch_model(id))
        self.db_session.delete(model)
        self.db_session.commit()
        self.deleted.send(model)
        return model

    def query(self, query, ctx=None):
        return self.authorize(ctx, 'query', self.filter_all(query))

    @property
    def db_session(self):
        return self.session_factory()

    def fetch_model(self, id):
        model = self.db_session.query(self.model).get(id)

        if not model:
            raise ModelNotFoundException(model_id=id, model_name=self.model_name)

        return model

    def fetch_all(self):
        return self.db_session.query(self.model).all()

    def filter_all(self, filter_dict):
        return self.db_session.query(self.model).filter_by(**filter_dict).all()
