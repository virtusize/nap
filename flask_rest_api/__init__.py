# -*- coding: utf-8 -*-

import json

from inflection import underscore, dasherize, pluralize
from flask import Blueprint
from flask.views import MethodView


class Api(Blueprint):

    def __init__(self, name, prefix, version):
        super(Api, self).__init__(name, name,
                                  url_prefix=prefix + '/v' + str(version))


class ModelView(MethodView):
    id_type = 'int'

    @classmethod
    def endpoint(cls):
        return '/' + dasherize(cls.model_name()) + '/'

    @classmethod
    def model_name(cls):
        return underscore(pluralize(cls.model.__name__))

    @classmethod
    def register_on(cls, api):
        view = cls.as_view(cls.model_name())
        endpoint_prefix = cls.endpoint()

        api.add_url_rule(endpoint_prefix, defaults={'id': None},
                          view_func=view, methods=['GET'])

        api.add_url_rule(endpoint_prefix,
                          view_func=view, methods=['POST'])

        api.add_url_rule(endpoint_prefix + '<%s:id>' % cls.id_type,
                          view_func=view, methods=['GET', 'PUT', 'DELETE'])

        api.add_url_rule(endpoint_prefix, view_func=view)


class ImplicitModelView(ModelView):

    def get(self, id=None):
        if id is None:
            return json.dumps([m.to_dict() for m in self.store._all()])
        else:
            return json.dumps(self.store._get(id).to_dict())
