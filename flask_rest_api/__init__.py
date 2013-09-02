# -*- coding: utf-8 -*-


from flask import Blueprint
from flask.views import MethodView


class Api(Blueprint):

    def __init__(self, name, prefix, version):
        super(Api, self).__init__(name, name, url_prefix=prefix + '/v' + str(version))

    def add_controller(self, controller):
        self.add_url_rule(controller.endpoint, view_func=controller.as_view())


class Controller(MethodView):

    def __init__(self, model):
        self.model = model

    @property
    def endpoint(self):
        return '/' + self.model.api_name() + '/'

    def as_view(self):
        return super(Controller, self).as_view(self.model.api_name())
