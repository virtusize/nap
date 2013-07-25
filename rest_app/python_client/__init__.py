# -*- coding: utf-8 -*-

from rest_app.python_client.resources import Todos


class Client(object):

    def __init__(self, base="http://localhost:5000"):

        self.base = base
        self.todos = Todos(base)
