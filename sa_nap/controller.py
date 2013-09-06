# -*- coding: utf-8 -*-
from nap.controller import BaseController


class SAModelController(BaseController):

    def __init__(self, model, session_factory):
        self.model = model
        self.session_factory = session_factory

    @property
    def db_session(self):
        return self.session_factory()

    def index(self, context=None):
        return self.db_session.query(self.model)

    def read(self, id, context=None):
        return self._get_model(id)

    def create(self, attributes, context=None):
        model = self.model(**attributes)
        self.db_session.add(model)
        self.db_session.commit()
        return model

    def update(self, id, attributes, context=None):
        model = self._get_model(id)
        model.update_attributes(attributes)
        self.db_session.commit()
        return model

    def delete(self, id, context=None):
        model = self._get_model(id)
        self.db_session.delete(model)
        self.db_session.commit()
        return model

    def _get_model(self, id):
        return self.db_session.query(self.model).get(id)
